# Generated by Django 3.1.3 on 2021-02-09 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20210209_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Product Type'),
        ),
    ]
