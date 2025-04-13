from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.models import AnonymousUser

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory, FavoritesProduct, Brand


class CatalogListView(TitleMixin, ListView):
    model = ProductCategory
    template_name = 'products/catalog-list.html'
    title = 'Arcitc Shop - Все категории'

    def get_queryset(self):
        return ProductCategory.objects.all()  # Возвращаем все категории продуктов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['favorites'] = FavoritesProduct.objects.filter(user=self.request.user)
            context['favorites_quantity'] = context['favorites'].count()
        else:
            context['favorites'] = []
            context['favorites_quantity'] = 0

        return context


class CatalogViewList(TitleMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    paginate_by = 2
    title = 'Store - Продукты'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')

        # Фильтрация по категории
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтрация по брендам
        brand_ids = self.request.GET.getlist('brands')
        if brand_ids:
            queryset = queryset.filter(brand_id__in=brand_ids)

        # Фильтрация по цене
        min_price = self.request.GET.get('min', 0)  # По умолчанию 0
        max_price = self.request.GET.get('max', 195000)  # По умолчанию 195000

        # Проверяем, если min и max цены - это строки, применяем replace и преобразуем в int
        try:
            min_price = int(str(min_price).replace(' ', '').replace(',', ''))
            max_price = int(str(max_price).replace(' ', '').replace(',', ''))
        except ValueError:
            # В случае ошибки возвращаем дефолтные значения
            min_price, max_price = 0, 195000

        # Применяем фильтрацию по цене
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogViewList, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(ProductCategory, id=category_id) if category_id else None

        context['category'] = category
        context['brands'] = Brand.objects.filter(products__category=category).distinct()
        context['request'] = self.request
        context['selected_brands'] = self.request.GET.getlist('brands')

        # Фильтрация по цене
        context['min_price'] = self.request.GET.get('min', 0)
        context['max_price'] = self.request.GET.get('max', 195000)

        if self.request.user.is_authenticated:
            context['favorites'] = FavoritesProduct.objects.filter(user=self.request.user)
            context['favorites_quantity'] = context['favorites'].count()
        else:
            context['favorites'] = []
            context['favorites_quantity'] = 0

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
        if isinstance(self.request.user, AnonymousUser):
            return Basket.objects.none()  # Возвращаем пустой queryset для анонимных пользователей
        return Basket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.request.user, AnonymousUser):
            context['favorites'] = []
            context['favorites_quantity'] = 0
        else:
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
