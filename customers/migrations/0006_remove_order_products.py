# Generated by Django 4.2.5 on 2023-09-18 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]