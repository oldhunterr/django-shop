from django.db import models
from users.models import User
from metadata.models import product_condition
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    condition = models.ForeignKey(product_condition, on_delete=models.CASCADE, related_name='products', null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='products')
    images = models.ImageField(blank=True, null=True, upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


