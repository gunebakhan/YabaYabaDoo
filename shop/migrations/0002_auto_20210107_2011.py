# Generated by Django 3.1.3 on 2021-01-07 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', related_query_name='shop', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payments', related_query_name='payments', to='shop.order', verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', related_query_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', related_query_name='order_items', to='shop.order', verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', related_query_name='order_items', to='shop.shopproduct', verbose_name='Shop Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', related_query_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='basketitem',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', related_query_name='basket_items', to='shop.basket', verbose_name='Basket'),
        ),
        migrations.AddField(
            model_name='basketitem',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', related_query_name='basket_items', to='shop.shopproduct', verbose_name='Shop Product'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', related_query_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]