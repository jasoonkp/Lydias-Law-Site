# Generated manually for OAuth scaffolding

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0006_appointment_cancellation_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalendlyOAuthToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("access_token", models.TextField()),
                ("refresh_token", models.TextField(blank=True, null=True)),
                ("token_type", models.CharField(default="Bearer", max_length=20)),
                ("scope", models.TextField(blank=True, null=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
    ]

