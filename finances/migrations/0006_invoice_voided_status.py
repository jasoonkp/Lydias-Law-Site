from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0005_invoice_hosted_invoice_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("PAID", "Paid"),
                    ("PAYMENT_FAILED", "Payment Failed"),
                    ("VOIDED", "Voided"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
