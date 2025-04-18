# Generated by Django 5.1.4 on 2025-03-26 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_featuredproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('products', models.ManyToManyField(related_name='featured_collections', to='products.product')),
            ],
            options={
                'verbose_name': 'Подборка товаров',
                'verbose_name_plural': 'Подборки товаров',
            },
        ),
        migrations.DeleteModel(
            name='FeaturedProducts',
        ),
    ]
