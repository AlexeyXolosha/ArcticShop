# Generated by Django 5.1.4 on 2025-03-24 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_preview', models.ImageField(blank=True, null=True, upload_to='news_image/')),
                ('title', models.CharField(max_length=255)),
                ('image_content', models.ImageField(blank=True, null=True, upload_to='news_image/')),
                ('min_description', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
