from django.contrib import admin
from .models import Advantages, News

@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(News)
class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
