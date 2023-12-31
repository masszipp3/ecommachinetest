# Generated by Django 4.2.5 on 2023-09-18 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_admin', '0005_alter_accounts_contact_number_alter_accounts_name'),
        ('customers', '0004_order_orderitem_order_products_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop_admin.address'),
        ),
    ]
