# Generated by Django 3.1.3 on 2021-02-16 21:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Slug')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Create')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Update')),
                ('details', models.TextField(verbose_name='Details')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Slug')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Create')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Update')),
                ('details', models.TextField(verbose_name='Details')),
                ('image', models.ImageField(upload_to='products/categpry', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('rate', models.IntegerField(choices=[(0, 'صفر'), (1, 'یک'), (2, 'دو'), (3, 'سه'), (4, 'چهار'), (5, 'پنج')], default=0, verbose_name='Rate')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publish')),
                ('draft', models.BooleanField(default=True, verbose_name='Draft')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.BooleanField(verbose_name='Condition')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
            ],
            options={
                'verbose_name': 'CommentLike',
                'verbose_name_plural': 'CommentLikes',
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='media/products/images/%Y/%m/%d', verbose_name='Image')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'ImageGallery',
                'verbose_name_plural': 'ImageGalleries',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='media/products', verbose_name='Image')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', related_query_name='product', to='products.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', related_query_name='product', to='products.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default='None', max_length=50, verbose_name='Height Width Length')),
                ('weight', models.CharField(default='None', max_length=50, verbose_name='Weight')),
                ('cpu_manufacturer', models.CharField(default='None', max_length=50, verbose_name='CPU Manufacturer')),
                ('cpu_series', models.CharField(default='None', max_length=50, verbose_name='CPU Series')),
                ('cpu_model', models.CharField(default='None', max_length=50, verbose_name='CPU Model')),
                ('cpu_speed', models.CharField(default='None', max_length=50, verbose_name='CPU Speed')),
                ('cach', models.CharField(default='0', max_length=50, verbose_name='Cach')),
                ('ram_capacity', models.CharField(default='None', max_length=50, verbose_name='RAM Capacity')),
                ('ram_type', models.CharField(default='None', max_length=50, verbose_name='RAM Type')),
                ('storage', models.CharField(default='None', max_length=50, verbose_name='Storage')),
                ('storage_type', models.CharField(default='None', max_length=50, verbose_name='Storage Type')),
                ('gpu_manufacturer', models.CharField(default='None', max_length=50, verbose_name='GPU Manufacturer')),
                ('gpu_model', models.CharField(default='None', max_length=50, verbose_name='GPU Model')),
                ('gpu_ram', models.CharField(default='None', max_length=50, verbose_name='GPU RAM')),
                ('display_size', models.CharField(default='None', max_length=50, verbose_name='Display Size')),
                ('display_type', models.CharField(default='None', max_length=50, verbose_name='Display Type')),
                ('display_accuracy', models.CharField(default='None', max_length=50, verbose_name='Display Accuracy')),
                ('display_mate', models.BooleanField(default=False, verbose_name='Display Mate')),
                ('display_touchable', models.BooleanField(default=False, verbose_name='Display Touchable')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta', related_query_name='meta', to='products.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'ProductMeta',
                'verbose_name_plural': 'ProductMetas',
            },
        ),
        migrations.CreateModel(
            name='MobileMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50, verbose_name='Size')),
                ('sim_card_desc', models.CharField(max_length=50, verbose_name='Sim Card Descrioption')),
                ('weight', models.CharField(max_length=50, verbose_name='Weight')),
                ('body_structure', models.CharField(max_length=50, verbose_name='Body Structur')),
                ('special_properties', models.CharField(max_length=50, verbose_name='Special Properties')),
                ('num_sim_cards', models.CharField(max_length=50, verbose_name='Num of Sim Cards')),
                ('intro_date', models.DateTimeField(verbose_name='Introduction Date')),
                ('slot_for_sim', models.CharField(choices=[('دارد', 'دارد'), ('ندارد', 'ندارد')], max_length=50, verbose_name='Slot For Sim')),
                ('model', models.CharField(max_length=50, verbose_name='Model')),
                ('cpu_chipset', models.CharField(max_length=250, verbose_name='CPU Chipset')),
                ('cpu', models.CharField(max_length=250, verbose_name='CPU')),
                ('cpu_type', models.CharField(max_length=50, verbose_name='CPU Type')),
                ('cpu_freequency', models.CharField(max_length=50, verbose_name='CPU Frequency')),
                ('gpu', models.CharField(max_length=50, verbose_name='GPU')),
                ('ram', models.CharField(max_length=50, verbose_name='RAM')),
                ('ram_capacity', models.CharField(max_length=50, verbose_name='RAM Capacity')),
                ('side_storage', models.CharField(max_length=50, verbose_name='Side Storage')),
                ('side_storage_standard', models.CharField(max_length=50, verbose_name='Side Storage Standard')),
                ('colorful_display', models.CharField(choices=[('بلی', 'بلی'), ('خیر', 'خیر')], max_length=50, verbose_name='Colorful Storage')),
                ('touchable_display', models.CharField(choices=[('بلی', 'بلی'), ('خیر', 'خیر')], max_length=50, verbose_name='Touchable Display')),
                ('display_techno', models.CharField(max_length=50, verbose_name='Display Techni')),
                ('display_size_range', models.CharField(max_length=50, verbose_name='Display Size Range')),
                ('display_size', models.CharField(max_length=50, verbose_name='Display Size')),
                ('resolution', models.CharField(max_length=50, verbose_name='Resolution')),
                ('pixel_density', models.CharField(max_length=50, verbose_name='Pixel Density')),
                ('display_to_body', models.CharField(max_length=50, verbose_name='Display to Body')),
                ('display_ratio', models.CharField(max_length=50, verbose_name='Display Ratio')),
                ('networks', models.CharField(max_length=50, verbose_name='Networks')),
                ('network_2g', models.CharField(max_length=250, verbose_name='2G Network')),
                ('network_3g', models.CharField(max_length=250, verbose_name='3G Network')),
                ('network_4g', models.CharField(max_length=250, verbose_name='4G Network')),
                ('connection_technology', models.CharField(max_length=250, verbose_name='Connection Technology')),
                ('wifi', models.CharField(max_length=250, verbose_name='Wi-Fi')),
                ('bluetooth', models.CharField(max_length=250, verbose_name='Bluetooth')),
                ('location_techno', models.CharField(max_length=250, verbose_name='Location Technology')),
                ('port', models.CharField(max_length=250, verbose_name='Port')),
                ('back_camera_modules', models.CharField(max_length=50, verbose_name='Back Camera Modules')),
                ('image_resolution', models.CharField(max_length=50, verbose_name='Image Resolution')),
                ('flash', models.CharField(max_length=50, verbose_name='Flash')),
                ('camera_capabalities', models.TextField(verbose_name='Camera Capabalities')),
                ('filming', models.CharField(max_length=250, verbose_name='Filming')),
                ('selfie_camera', models.CharField(max_length=1024, verbose_name='Selfie Camera')),
                ('speaker', models.CharField(choices=[('بلی', 'بلی'), ('خیر', 'خیر')], max_length=50, verbose_name='Speaker')),
                ('voice_output', models.CharField(max_length=50, verbose_name='Voice Output')),
                ('os', models.CharField(max_length=50, verbose_name='OS')),
                ('os_release', models.CharField(max_length=50, verbose_name='OS Realease')),
                ('software_capabalities', models.TextField(verbose_name='Software Capabalities')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mobile_meta', related_query_name='mobile_meta', to='products.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'MobileMeta',
                'verbose_name_plural': 'MobileMetas',
            },
        ),
        migrations.CreateModel(
            name='LikeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.BinaryField(blank=True, null=True, verbose_name='Condition')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', related_query_name='likes', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'LikeProduct',
                'verbose_name_plural': 'LikeProducts',
            },
        ),
    ]
