from rest_framework.routers import DefaultRouter
from .views import TourViewSet, CategoryViewSet, CountryViewSet, BookingViewSet, UserViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'tours', TourViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]