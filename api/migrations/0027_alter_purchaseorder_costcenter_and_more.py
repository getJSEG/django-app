# Generated by Django 4.2.7 on 2025-03-19 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_expense_totalamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='costCenter',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='datePaid',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
