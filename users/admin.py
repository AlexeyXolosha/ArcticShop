from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from products.admin import BasketAdmin
from users.models import EmailVerification, User

# Register your models here.

# Регистрация User с защитой от двойного импорта
try:
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        list_display = ('first_name', 'email')
        inlines = (BasketAdmin,)
except AlreadyRegistered:
    pass

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'user')
        }),
        ('Даты', {
            'fields': ('expiration', 'created'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created',)
