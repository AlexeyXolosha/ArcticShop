# Generated by Django 5.1.4 on 2025-03-24 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_brand_product_brand_productcategory_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_banners/')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='products.product')),
            ],
            options={
                'verbose_name': 'Баннер продукта',
                'verbose_name_plural': 'Баннеры продуктов',
            },
        ),
    ]
