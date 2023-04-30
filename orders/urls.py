from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('signup/',views.signup_user,name="signup_user"),
    path('login/',views.login_user,name="login_user"),
    path('all_categories/',views.all_categories,name="all_categories"),
    path('show_category/<int:id>/',views.show_category,name="show_category"),
    path('show_dish/<int:id>/',views.show_dish,name="show_dish"),
    path('show_cart/',views.show_cart,name="show_cart"),
    path('add_to_cart/<int:id>',views.add_to_cart,name="add_to_cart"),
    path('delete_from_cart/<int:id>',views.delete_from_cart,name="delete_from_cart"),
    path('change_amount/<int:id>',views.change_amount,name="change_amount"),
    path('create_delivery/',views.create_delivery,name="create_delivery"),
    path('delivery_details/',views.create_delivery,name="create_delivery"),
    path('user_delivery_confirmation/<int:id>',views.user_delivery_confirmation,name="user_delivery_confirmation"),
    path('order_history/',views.order_history,name="order_history"),
    path('update_user/<int:id>',views.update_user,name="update_user"),
    path('logout/',views.logout_user,name="logout_user")
    ]