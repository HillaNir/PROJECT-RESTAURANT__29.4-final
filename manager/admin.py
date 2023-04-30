from django.contrib import admin
from orders.models import User, Cart, Category, Dish, Delivery, Item

# Register your models here.
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Delivery)
admin.site.register(Item)