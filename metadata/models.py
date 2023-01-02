from django.db import models

# Create your models here.
class product_condition(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class product_status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name