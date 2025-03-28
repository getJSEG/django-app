# Generated by Django 4.2.7 on 2025-03-13 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreceipt',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'Avierto'), ('CLOSED', 'Cerrado'), ('PAID', 'Pagado'), ('PROCESSING', 'procesando'), ('CANCELED', 'Cancelado')], default='Avierto', max_length=25, null=True),
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shippingType', models.CharField(choices=[('PersonaShipping', 'Envio Personalizado'), ('parsel', 'Encomienda')], max_length=255)),
                ('ShippintReceipts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ShippingReceites', to='api.salesreceipt')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ParselShipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('PREPAIDED', 'Pagado'), ('PROCESSING', 'procesando'), ('SHIPPED', 'Enviado'), ('PICKEDUP', 'Recojido'), ('NOSHOW', 'No Retiro'), ('CANCELED', 'Cancelado')], default='procesando', max_length=25, null=True)),
                ('name', models.CharField(max_length=255)),
                ('attempts', models.IntegerField()),
                ('comment', models.CharField(max_length=255)),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shipping')),
            ],
        ),
        migrations.CreateModel(
            name='CustomShipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('PREPAIDED', 'Pagado'), ('PROCESSING', 'procesando'), ('SHIPPED', 'Enviado'), ('DELIVERED', 'Entregado'), ('CANCELED', 'Cancelado')], default='procesando', max_length=25, null=True)),
                ('name', models.CharField(max_length=255)),
                ('attempts', models.IntegerField()),
                ('comment', models.CharField(max_length=255)),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shipping')),
            ],
        ),
    ]
