# Generated by Django 4.2.5 on 2023-09-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_admin', '0002_accounts_address_remove_categories_shop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Product_ID',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
    ]
