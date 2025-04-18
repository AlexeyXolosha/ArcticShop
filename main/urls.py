from django.urls import path, include
from views import IndexView

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', include('products.urls')),
]
