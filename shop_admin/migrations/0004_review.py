# Generated by Django 4.2.5 on 2023-09-17 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_admin', '0003_alter_product_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.CharField(max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_admin.accounts')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_admin.product')),
            ],
        ),
    ]
