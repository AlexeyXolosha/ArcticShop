from django.shortcuts import render
from django.views.generic import TemplateView
from main.models import Advantages, News
from products.models import ProductCategory, Brand
from common.views import TitleMixin

# Create your views here.

class IndexView(TitleMixin, TemplateView):
    template_name = 'main/index.html'
    title = 'Arctic Store - Главная Страница'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['brands'] = Brand.objects.all()
        context['news'] = News.objects.all()
        return context