# Generated by Django 4.2.7 on 2024-04-13 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_locations_store_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_code',
            field=models.CharField(max_length=56, unique=True),
        ),
    ]