from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory, FavoritesProduct


class CatalogViewList(TitleMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    paginate_by = 2
    title = 'Store - Продукты'

    def get_queryset(self):
        queryset = super(CatalogViewList, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogViewList, self).get_context_data(**kwargs)
        context['category'] = ProductCategory.objects.all()
        return context

@login_required
def favorites_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = FavoritesProduct.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.quantity += 1
        favorite.save()
        favorite.delete()
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def favorites_remove(request, product_id):
    favorite = FavoritesProduct.objects.filter(user=request.user, product_id=product_id).first()

    if favorite:
        favorite.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class BasketView(ListView):
    model = Basket
    template_name = 'products/baskets.html'
    context_object_name = 'baskets'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = FavoritesProduct.objects.filter(user=self.request.user)
        context['favorites_quantity'] = context['favorites'].count()  # Подсчитываем количество
        return context

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

        ### Возвращаем пользователя на ту же страницу где он и был при добавлении товара, или же при его увелечении
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
