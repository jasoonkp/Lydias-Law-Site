# Generated manually for LLW-63

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0005_invitee_phone_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointments",
            name="cancellation_reason",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="appointments",
            name="cancelled_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

