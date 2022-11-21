from django.contrib import admin
from .models import Product, category
# Register your models here.

admin.site.register(category)
admin.site.register(Product)