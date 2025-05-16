from rest_framework import viewsets, permissions, filters
from .serializers import TourSerializer, CategorySerializer, CountrySerializer, BookingSerializer, UserSerializer
from main.models import Tour, Category, Country, Booking, User
from .permissions import IsOwnerOrReadOnly 

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]