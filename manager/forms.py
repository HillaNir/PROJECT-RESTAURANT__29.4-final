from django import forms
from orders.models import Dish, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'imageUrl']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'price', 'description', 'imageUrl']


# class DishForm(forms.ModelForm):
#     is_gluten_free = forms.BooleanField(required=False)
#     is_vegetarian = forms.BooleanField(required=False)

#     class Meta:
#         model = Dish
#         fields = ['name', 'price', 'description', 'imageUrl', 'is_gluten_free', 'is_vegetarian']
#         widgets = {
#             'is_gluten_free': forms.CheckboxInput(),
#             'is_vegetarian': forms.CheckboxInput(),
#         }