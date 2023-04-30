from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import NewUserCreationForm, EditUserForm
from .models import User, Cart, Category, Delivery, Dish, Item
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def index(request):
    return render(request,'orders/index.html')


def signup_user(request):
    form = NewUserCreationForm()
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your new user has been created successfully!'))
            return redirect('login_user')
    return render(request, 'orders/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
                            )
        if user is not None:
            login(request,user)
            return redirect('all_categories')
        else: # אם לא מצאת יוזר
            return HttpResponse('Login failed - invalid username or password.')
    else: # אם זאת לא בקשת פוסט
        return render(request, 'orders/login.html')


def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details has been updated.")
            return redirect('all_categories')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'orders/update_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url="login")
def all_categories(request):
    all_categories = Category.objects.all()
    return render(request,'orders/all_categories.html',{"categories":all_categories})


@login_required(login_url="login")
def show_category(request, id):
    category = Category.objects.get(id=id)
    return render(request,'orders/show_category.html',{"category":category})


@login_required(login_url="login")
def show_dish(request, id):
    dish = Dish.objects.get(id=id)
    category = dish.category
    return render(request,'orders/show_dish.html',{"dish":dish, "category":category})
    

@login_required(login_url="login")
def add_to_cart(request, id):
    user = request.user
    dish = Dish.objects.get(id=id)
    carts = [cart for cart in request.user.cart_set.all()]
    if not carts: # אם אין לו עגלות
        new_cart = Cart(user=user)
        new_cart.save()
        amount = int(request.POST.get('amount', 0))
        new_item = Item(
            dish=dish,
            cart=new_cart,
            amount=amount
        )
        new_item.save()
        items = new_cart.item_set.all()
        total = calculate_total(items)
        return render(request, 'orders/show_cart.html', {"cart": new_cart,"items": items, "total": total})
    else: # אם יש לו עגלות
        for item in carts[-1].item_set.all(): # תרוץ על כל האיטמים בעגלה
            if item.dish.id == dish.id: # אם מצאת התאמה, תעלה את הכמות
                amount = int(request.POST.get('amount', 0))
                item.amount += amount
                item.save()
                items = carts[-1].item_set.all()
                total = calculate_total(items)
                return render(request, 'orders/show_cart.html', {"cart": carts[-1], "items": items, "total": total})
        else: # אם האייטם לא בעגלה, תוסיף חדש ממנו
            amount = int(request.POST.get('amount', 0))
            new_item = Item(
                dish=dish,
                cart=carts[-1],
                amount=amount
            )
            new_item.save()
            items = carts[-1].item_set.all()
            total = calculate_total(items)
            return render(request, 'orders/show_cart.html', {"cart": carts[-1], "items": items, "total": total})


@login_required(login_url="login")
def show_cart(request):
    carts = [cart for cart in request.user.cart_set.all()]
    if not carts: # אם אין עגלות
        cart = None
        items = None
        total = None
    else: # אם יש עגלות
        cart = carts[-1]
        items = cart.item_set.all()
        total = calculate_total(items)
        for item in items:
            item.total_cost = item.amount * item.dish.price
            # להוסיף אופציה של מחיקת מוצר, והגדלת כמות או להעביר בעמוד של עריכת עגלה בבקשת פוסט
        cart.total = total
        cart.save()
    return render(request, 'orders/show_cart.html', {"cart": cart, "items" : items, "total" :total})


def calculate_total(items):
    total = sum((item.amount * item.dish.price) for item in items) 
    return total


@login_required(login_url="login")
def delete_from_cart(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('show_cart')


@login_required(login_url="login")
def change_amount(request, id):
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount >= 1 and amount <= 10:
            item.amount = amount
            item.save()
    return redirect('show_cart')


@login_required(login_url="login")
def create_delivery(request):
    user = request.user
    carts = [cart for cart in request.user.cart_set.all()]
    cart = carts[-1]
    if request.method == 'POST':
        address = request.POST.get('address')
        comment = request.POST.get('comment')
        if address and comment: # נוודא שהשדות באמת מלאים
            try:
                delivery = cart.delivery
            except Delivery.DoesNotExist:
                delivery = None
            if not delivery: # אם אין משלוח משויך לעגלה
                if not user.is_staff:
                    delivery = Delivery(
                    cart = cart,
                    address = address,
                    comment = comment,
                    is_delivered = False,
                    created = datetime.now()
                    )
                    delivery.save()
                    messages.success(request, 'Delivery created successfully!')
                    return render(request,'orders/user_delivery_confirmation.html', {"delivery" : delivery})
                else:
                    new_cart = Cart(user = user)
                    new_cart.save()
                    delivery = Delivery(
                    cart=new_cart,
                    address="Staff member",
                    comment="No delivery required",
                    is_delivered=False,
                    created=datetime.now()
                    )
                    delivery.save()
                    return redirect('all_categories')                    
            else: # אם לעגלה משויך משלוח
                if delivery.is_delivered:
                    new_cart = Cart(user=user)
                    new_cart.save()
                    redirect('all_categories')
                else:
                    return HttpResponse('Please wait for the previous delivery to be confirmed.')
    return render(request,'orders/delivery_details.html')    


@login_required(login_url="login")
def user_delivery_confirmation(request, id):
    user = request.user
    delivery = Delivery.objects.get(cart_id=id, cart__user=user, is_delivered=False)
    total = calculate_total(delivery.cart.item_set.all())
    delivery.total = total
    delivery.save()
    return render(request, 'orders/user_delivery_confirmation.html', {"delivery" : delivery, "total" : total})


@login_required(login_url="login")
def order_history(request):
    deliveries = Delivery.objects.filter(cart__user=request.user).order_by('-created')
    if not deliveries:
        return render(request, 'orders/order_history.html')
    else:
        for delivery in deliveries:
            total = calculate_total(delivery.cart.item_set.all())
            delivery.total = total
    return render(request, 'orders/order_history.html', {"deliveries": deliveries})
