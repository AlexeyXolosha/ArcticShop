from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from unicodedata import category

from products.models import ProductCategory, Product, Basket
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_num=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 2
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_num)

    context = {
        'title': 'Store-Каталог',
        'category': ProductCategory.objects.all(),
        'products': products_paginator,
    }
    return render(request, 'products/products.html', context)


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
