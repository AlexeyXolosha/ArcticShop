from django.urls import path

from products.views import CatalogViewList, BasketView, basket_add, basket_remove, favorites_add, favorites_remove

app_name = 'products'

urlpatterns = [
    path('category/<int:category_id>/', CatalogViewList.as_view(), name='category'),

    path('page/<int:page>/', CatalogViewList.as_view(), name='paginator'),

    path('favorite/add/<int:product_id>/', favorites_add, name='toggle_favorite'),

    path('favorite/remove/<int:product_id>/', favorites_remove, name='favorites_remove'),

    path('baskets', BasketView.as_view(), name='baskets'),

    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
