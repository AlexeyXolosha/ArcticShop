from django.contrib import admin

from products.models import Basket, Product, ProductCategory, Brand, ProductBanner, FeaturedProduct

# Register your models here.
admin.site.register(ProductCategory)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'brand')
    fields = ('name', 'description', ('price', 'quantity'), "image", "category", "brand")  # Добавили brand
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProductBanner)
class ProductBanner(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(FeaturedProduct)
class FeaturedProducts(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
