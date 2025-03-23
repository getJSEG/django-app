# Generated by Django 4.2.7 on 2025-03-19 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_rename_location_id_expense_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='totalAmount',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=10),
            preserve_default=False,
        ),
    ]
