# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('map/', views.map_view, name='map'),
    path('products/', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:tour_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:tour_id>/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/history/', views.order_history, name='order_history'),
    ]