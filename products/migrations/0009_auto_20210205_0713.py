# Generated by Django 3.1.3 on 2021-02-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20210205_0711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AddField(
            model_name='productmeta',
            name='color',
            field=models.CharField(choices=[('black', 'Black'), ('white', 'white'), ('pink', 'Pink'), ('red', 'Red'), ('green', 'Green'), ('yellow', 'Yellow')], default='black', max_length=100, verbose_name='Color'),
        ),
    ]
