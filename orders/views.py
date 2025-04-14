from django.shortcuts import render
from django.views.generic import TemplateView

from common.views import TitleMixin
from django.views.generic.list import ListView


# Create your views here.
class OrderCreateView(TitleMixin, TemplateView):
    template_name = 'orders/order-create.html'
    title = 'Arcitc Shop - Создание заказа'


