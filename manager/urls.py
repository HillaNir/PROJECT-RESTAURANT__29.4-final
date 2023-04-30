from django.urls import path
from . import views

urlpatterns = [
    path('all_users/',views.all_users,name="all_users"),
    path('all_deliveries/', views.all_deliveries, name='all_deliveries'),
    path('add_dish/<int:id>', views.add_dish, name='add_dish'),
    path('edit_dish/<int:id>/', views.edit_dish, name='edit_dish'),
    path('delete_dish/<int:id>/', views.delete_dish, name='delete_dish'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

]