from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    imageUrl = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Delivery(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, primary_key=True)
    is_delivered = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=False)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    price = models.IntegerField(blank=False)
    description = models.TextField(blank=True)
    imageUrl = models.TextField(blank=True)
    is_gluten_free = models.BooleanField(blank=False, default=False)
    is_vegeterian = models.BooleanField(blank=False, default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(default=1)
