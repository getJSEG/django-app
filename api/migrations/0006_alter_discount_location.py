# Generated by Django 4.2.7 on 2024-04-14 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_discount_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.locations'),
        ),
    ]
