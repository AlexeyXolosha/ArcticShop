from django.shortcuts import render
from django.views.generic import TemplateView
from main.models import Advantages, News
from products.models import ProductCategory, ProductBanner, Brand, FavoritesProduct, FeaturedProduct
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
        context['advantages'] = Advantages.objects.all()
        context['banner'] = ProductBanner.objects.all()
        context['hit'] = FeaturedProduct.objects.filter(name="Хиты продаж").first()
        if self.request.user.is_authenticated:
            context['favorites'] = FavoritesProduct.objects.filter(user=self.request.user)
        else:
            context['favorites'] = []
        return context
