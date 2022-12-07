from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('product/search', views.search, name='search'),
    path('product/<int:id>', views.productview, name='productview'),
    path('product/add', views.add, name='add'),
    # path('product/<int:id>', views.product, name='product'),
]
