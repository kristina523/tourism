from rest_framework import serializers
from main.models import Tour, Category, Country, Booking, User

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'country', 'category', 'price', 'duration_days', 'start_date', 'end_date', 'max_participants', 'is_active', 'created_at', 'image_url', 'is_hot']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'image_url']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name', 'description', 'visa_requirements']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'tour', 'booking_date', 'participants', 'total_price', 'status', 'notes']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'groups', 'user_permissions']