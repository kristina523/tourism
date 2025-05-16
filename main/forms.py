from django import forms
from .models import Category, Tour
from .models import Order
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'image_url']

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'title', 'description', 'country', 'category', 'price',
            'duration_days', 'start_date', 'end_date', 'max_participants', 'image_url'
        ]
class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
    reload = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=False)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_method', 'address']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "phone", "password1", "password2")

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)