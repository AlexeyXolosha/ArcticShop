from django.db import models

from users.models import User


class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def __str__(self):
    return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория {self.category.name}'


class FeaturedProduct(models.Model):
    name = models.CharField(max_length=128, unique=True)
    products = models.ManyToManyField("Product",
                                      related_name="featured_collections")  # Связь многие-ко-многим с продуктами

    class Meta:
        verbose_name = "Подборка товаров"
        verbose_name_plural = "Подборки товаров"

    def __str__(self):
        return f"{self.name} ({self.get_product_count()} товаров)"

    def get_product_count(self):
        return self.products.count() 


class ProductBanner(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='product_banners/')
    title = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Баннер продукта'
        verbose_name_plural = 'Баннеры продуктов'

    def __str__(self):
        return f'Баннер для {self.product.name}'


class FavoritesProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")
    quantity = models.PositiveSmallIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"

    def __str__(self):
        return f"{self.user.email} → {self.product.name}"


class BasketQuerySet(models.query.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Продукт: {self.user.email} | Категория: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
