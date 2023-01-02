from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('product/search', views.search, name='search'),
    path('product/filter', views.product_filter, name='filter'),
    path('product/<int:id>', views.show, name='productview'),
    path('product/<int:id>/edit', views.edit, name='edit'),
    path('product/create', views.create, name='add'),
    path('product/<int:id>/delete', views.delete, name='delete'),
    # path('product/<int:id>', views.product, name='product'),
]
