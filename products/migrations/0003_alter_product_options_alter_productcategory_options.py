# Generated by Django 5.1.4 on 2025-02-14 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Категории', 'verbose_name_plural': 'Категории'},
        ),
    ]
