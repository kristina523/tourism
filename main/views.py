from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Order, OrderItem
from .cart import Cart
from .forms import CartAddForm, OrderCreateForm
from django.contrib.auth.decorators import login_required
from .forms import TourForm
from .models import Category
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import logout
from django.contrib.auth import login
from .forms import CategoryForm

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def map_view(request):
    return render(request, 'main/map.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'main/categories.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'main/category_detail.html', {'category': category})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'main/add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'main/edit_category.html', {'form': form, 'category': category})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'main/delete_category.html', {'category': category})


def products(request):
    products = Tour.objects.all()
    return render(request, 'main/products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Tour, pk=pk)
    cart_add_form = CartAddForm()
    return render(request, 'main/product_detail.html', {'product': product, 'cart_add_form': cart_add_form})

def add_product(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = TourForm()
    return render(request, 'main/add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = TourForm(instance=product)
    return render(request, 'main/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'main/delete_product.html', {'product': product})
# --- Каталог ---

def catalog(request):
    products = Tour.objects.all()
    return render(request, 'main/catalog.html', {'products': products})

def cart_add(request, tour_id):
    cart = Cart(request)
    tour = get_object_or_404(Tour, id=tour_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(tour=tour, quantity=cd['quantity'], reload=cd['reload'])
    return redirect('cart')

def cart_remove(request, tour_id):
    cart = Cart(request)
    tour = get_object_or_404(Tour, id=tour_id)
    cart.remove(tour)
    return redirect('cart')

def cart(request):
    cart = Cart(request)
    return render(request, 'main/cart.html', {'cart': cart})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    tour=item['tour'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            cart.clear()
            return render(request, 'main/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'main/order_create.html', {'cart': cart, 'form': form})
@login_required
def profile(request):
    user = request.user
    # Получаем все заказы пользователя
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'main/profile.html', {'user': user, 'orders': orders})
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # или 'home'
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # или 'home'
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})