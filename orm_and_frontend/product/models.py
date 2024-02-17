from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProductTable(models.Model):
    CATEGORIES = ((1,'Sneaker/Shoes'),(2,'Juti'),(3,'Bags'),(4,'Boots/Sandals'),(5,'Belts'))
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length =50)
    price = models.FloatField()
    details = models.CharField(max_length =100)
    category = models.IntegerField(choices = CATEGORIES)
    is_active = models.BooleanField()
    rating = models.FloatField(null=True)
    size  = models.CharField(max_length=10,null=True) #add null for
    image=models.ImageField(upload_to='image')

    def __str__(self):
        return "product " + self.name
    
class CartTable(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE,db_column='uid')
    pid = models.ForeignKey(ProductTable, on_delete = models.CASCADE,db_column='pid')
    quantity = models.IntegerField(default = 1)