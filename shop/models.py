from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='products')
    images = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
