from django.contrib import admin
from .models import *
# Register your models here.

class ImageAdmin(admin.StackedInline):
    model = extra_images
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = Product
admin.site.register(category)
admin.site.register(Product, ProductAdmin)
admin.site.register(extra_images)
# admin.site.register(product_condition)