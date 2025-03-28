# Generated by Django 4.2.7 on 2025-03-15 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_cashpayment_paymentmethod_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashpayment',
            name='id',
        ),
        migrations.RemoveField(
            model_name='creditcardpayment',
            name='id',
        ),
        migrations.RemoveField(
            model_name='transferpayment',
            name='id',
        ),
        migrations.AlterField(
            model_name='cashpayment',
            name='paymentMethod',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cashPaymentMethod', serialize=False, to='api.paymentmethod'),
        ),
        migrations.AlterField(
            model_name='creditcardpayment',
            name='paymentMethod',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='creditcardPaymentMethod', serialize=False, to='api.paymentmethod'),
        ),
        migrations.AlterField(
            model_name='transferpayment',
            name='paymentMethod',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='transferPaymentMethod', serialize=False, to='api.paymentmethod'),
        ),
    ]
