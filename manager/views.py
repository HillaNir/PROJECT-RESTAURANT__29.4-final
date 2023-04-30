from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DishForm, CategoryForm
from orders.models import Dish, Category, User, Delivery, Cart
from django.contrib import messages
from orders.views import calculate_total
from django.urls import reverse

# Create your views here.

@staff_member_required(login_url="all_categories")
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('show_category', id=category.id)
    return render(request,'manager/add_category.html',{"form":form})


@staff_member_required(login_url="all_categories")
def edit_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"{category.name} category has been updated.")
            return redirect('show_category', id=category.id)
    return render(request, 'manager/edit_category.html', {'form': form, 'category': category})


@staff_member_required(login_url="all_categories")
def delete_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        category.delete()
        return redirect('all_categories')


@staff_member_required(login_url="all_categories")
def add_dish(request, id):
    form = DishForm()
    category = Category.objects.get(id=id)
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False) # מייצרים אובייקט של מנה מהטופס שיצרתי, אבל לא שומרים בדאטה בייס
            dish.category = category # משייכים למנה קודם כל קטגוריה
            is_gluten_free = request.POST.get("is_gluten_free")
            is_vegeterian = request.POST.get("is_vegeterian")
            dish.is_gluten_free = True if is_gluten_free else False
            dish.is_vegeterian = True if is_vegeterian else False
            dish.save() # רק כאן נשמור את המנה
            messages.success(request, f"{dish.name} has been added to the menu.")
            return redirect('show_dish', id=dish.id)
    return render(request,'manager/add_dish.html',{"form":form, "category": category})



@staff_member_required(login_url="all_categories")
def edit_dish(request, id):
    dish = Dish.objects.get(id=id)
    form = DishForm(instance=dish)
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            dish = form.save(commit=False)
            is_gluten_free = request.POST.get("is_gluten_free")
            is_vegeterian = request.POST.get("is_vegeterian")
            dish.is_gluten_free = True if is_gluten_free else False
            dish.is_vegeterian = True if is_vegeterian else False
            dish.save()        
            messages.success(request, f"{dish.name} has been updated.")
            return redirect('show_dish', id=dish.id)
    return render(request, 'manager/edit_dish.html', {'form': form, 'dish': dish})


@staff_member_required(login_url="all_categories")
def delete_dish(request, id):
    dish = Dish.objects.get(id=id)
    category = Category.objects.get(id=dish.category.id)
    if request.method == 'POST':
        dish.delete()
        return render(request, 'orders/show_category.html', {'category': category})


@staff_member_required(login_url="all_categories")
def all_users(request):
    users = User.objects.all()    
    return render(request, 'manager/all_users.html', {"users" : users})


@staff_member_required(login_url="all_categories")
def all_deliveries(request):
    if request.method == 'POST':
        delivery = Delivery.objects.get(cart_id=request.POST['id'])
        delivery.is_delivered = True
        delivery.save()
        messages.success(request, f'Delivery #{delivery.cart_id} marked as delivered.')
        return redirect(reverse('all_deliveries'))
    
    all_deliveries = Delivery.objects.all()
    for delivery in all_deliveries:
        total = calculate_total(delivery.cart.item_set.all())
        delivery.total = total
    return render(request, 'manager/all_deliveries.html', {"all_deliveries": all_deliveries, "total": total})