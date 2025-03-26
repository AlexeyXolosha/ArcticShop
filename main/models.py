from django.db import models

# Create your models here.

class Advantages(models.Model):
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128, null=True, blank=True)
    image = models.FileField(upload_to='advantages/', null=True, blank=True)
    color = models.CharField(max_length=7, default="#6a0dad")

    class Meta:
        verbose_name = 'Преимущества'
        verbose_name_plural = 'Преимущества'

    def __str__(self):
        return self.name


class News(models.Model):
    image_preview = models.ImageField(upload_to='news_image/', null=True, blank=True)
    title = models.CharField(max_length=255)
    image_content = models.ImageField(upload_to='news_image/', null=True, blank=True)
    min_description = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
