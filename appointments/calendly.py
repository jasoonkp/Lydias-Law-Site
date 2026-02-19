import json
import logging
import os
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
from typing import Optional, Tuple

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

CALENDLY_OAUTH_AUTHORIZE_URL = "https://auth.calendly.com/oauth/authorize"
CALENDLY_OAUTH_TOKEN_URL = "https://auth.calendly.com/oauth/token"


def _calendly_api_enabled() -> bool:
    # Prefer settings, but also allow env override for local testing
    raw = getattr(settings, "CALENDLY_API_ENABLED", None)
    if raw is None:
        raw = os.environ.get("CALENDLY_API_ENABLED", "0")
    return str(raw).strip().lower() in {"1", "true", "yes", "y", "on"}


def calendly_api_enabled() -> bool:
    return _calendly_api_enabled()


def build_oauth_authorize_url(*, redirect_uri: str, state: Optional[str] = None, scope: Optional[str] = None) -> str:
    client_id = getattr(settings, "CALENDLY_CLIENT_ID", "") or os.environ.get("CALENDLY_CLIENT_ID", "")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    if state:
        params["state"] = state
    if scope:
        params["scope"] = scope
    return f"{CALENDLY_OAUTH_AUTHORIZE_URL}?{urlencode(params)}"


def _token_request(data: dict) -> dict:
    body = urlencode(data).encode("utf-8")
    req = Request(
        CALENDLY_OAUTH_TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)


def exchange_code_for_token(*, code: str, redirect_uri: str) -> dict:
    client_id = getattr(settings, "CALENDLY_CLIENT_ID", "") or os.environ.get("CALENDLY_CLIENT_ID", "")
    client_secret = getattr(settings, "CALENDLY_CLIENT_PASSWORD", "") or os.environ.get("CALENDLY_CLIENT_PASSWORD", "")
    return _token_request(
        {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
    )


def refresh_access_token(*, refresh_token: str) -> dict:
    client_id = getattr(settings, "CALENDLY_CLIENT_ID", "") or os.environ.get("CALENDLY_CLIENT_ID", "")
    client_secret = getattr(settings, "CALENDLY_CLIENT_PASSWORD", "") or os.environ.get("CALENDLY_CLIENT_PASSWORD", "")
    return _token_request(
        {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
    )


def upsert_oauth_token(token_data: dict) -> None:
    """
    Persist Calendly OAuth token response to DB (best effort).
    """
    try:
        from .models import CalendlyOAuthToken

        expires_in = token_data.get("expires_in")
        expires_at = None
        if isinstance(expires_in, int):
            expires_at = timezone.now() + timedelta(seconds=expires_in)

        CalendlyOAuthToken.objects.create(
            access_token=token_data.get("access_token", ""),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type") or "Bearer",
            scope=token_data.get("scope"),
            expires_at=expires_at,
        )
    except Exception:
        logger.exception("Failed to persist Calendly OAuth token (best effort).")


def _get_db_token() -> Optional[Tuple[str, Optional[str], Optional[datetime]]]:
    try:
        from .models import CalendlyOAuthToken

        tok = CalendlyOAuthToken.objects.order_by("-updated_at").first()
        if not tok:
            return None
        return tok.access_token, tok.refresh_token, tok.expires_at
    except Exception:
        return None


def get_access_token() -> Optional[str]:
    """
    Return an access token from env or DB, optionally refreshing if expired (best effort).
    """
    env_token = getattr(settings, "CALENDLY_ACCESS_TOKEN", "") or os.environ.get("CALENDLY_ACCESS_TOKEN", "")
    if env_token:
        return env_token

    db = _get_db_token()
    if not db:
        return None
    access_token, refresh_token, expires_at = db
    if not access_token:
        return None

    if expires_at and expires_at <= timezone.now() and refresh_token:
        try:
            token_data = refresh_access_token(refresh_token=refresh_token)
            upsert_oauth_token(token_data)
            return token_data.get("access_token") or access_token
        except Exception:
            logger.exception("Calendly token refresh failed (best effort).")
            return access_token

    return access_token


def cancel_scheduled_event(*, calendly_event_uri: str, cancellation_reason: str) -> bool:
    """
    Best-effort cancellation of a Calendly scheduled event.

    Safe for local/offline dev: if CALENDLY_API_ENABLED is false, we log and no-op.
    """
    if not calendly_event_uri:
        return False

    if not _calendly_api_enabled():
        logger.info("Calendly cancellation skipped (site not live yet — expected). event_uri=%s", calendly_event_uri)
        return False

    access_token = get_access_token()
    if not access_token:
        logger.warning(
            "Calendly API enabled but no access token configured; skipping cancellation. event_uri=%s",
            calendly_event_uri,
        )
        return False

    cancel_url = calendly_event_uri.rstrip("/") + "/cancellation"
    payload = {"reason": cancellation_reason or "Cancelled by admin"}
    req = Request(
        cancel_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=15) as resp:
            ok = 200 <= resp.status < 300
            if ok:
                logger.info("Calendly event cancelled via API. event_uri=%s", calendly_event_uri)
            else:
                logger.warning(
                    "Calendly cancel returned non-2xx. status=%s event_uri=%s",
                    resp.status,
                    calendly_event_uri,
                )
            return ok
    except HTTPError as e:
        logger.warning("Calendly cancel HTTPError. status=%s event_uri=%s", getattr(e, "code", None), calendly_event_uri)
        return False
    except URLError as e:
        logger.warning("Calendly cancel URLError. reason=%s event_uri=%s", e.reason, calendly_event_uri)
        return False
    except Exception:
        logger.exception("Calendly cancel unexpected error. event_uri=%s", calendly_event_uri)
        return False

