# Generated by Django 3.1.3 on 2021-01-08 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_view', '0003_auto_20210108_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='url',
            field=models.URLField(default="'https://google.com", verbose_name='Url'),
        ),
    ]