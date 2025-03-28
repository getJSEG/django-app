# Generated by Django 4.2.7 on 2025-03-17 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rename_neighborhood_customer_extradetails_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customshipping',
            old_name='comment',
            new_name='details',
        ),
        migrations.RenameField(
            model_name='parselshipping',
            old_name='comment',
            new_name='details',
        ),
        migrations.AlterField(
            model_name='customshipping',
            name='shippingType',
            field=models.CharField(choices=[('PersonalShipping', 'Envio Personalizado'), ('parsel', 'Encomienda')], max_length=25),
        ),
        migrations.AlterField(
            model_name='parselshipping',
            name='shippingType',
            field=models.CharField(choices=[('PersonalShipping', 'Envio Personalizado'), ('parsel', 'Encomienda')], max_length=25),
        ),
    ]
