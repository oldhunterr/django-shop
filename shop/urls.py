from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('product/search', views.search, name='search'),
    path('product/<int:id>', views.show, name='productview'),
    path('product/create', views.create, name='add'),
    # path('product/<int:id>', views.product, name='product'),
]
