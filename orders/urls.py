from django.urls import path

from .views import OrderCreateView

app_name = 'orders'  # Добавить это


urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
]
