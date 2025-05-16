from django.contrib import admin
from .models import (
    User,
    Country,
    Category,
    Tour,
    Booking,
    Review,
    Payment,
    Cart,
)

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Cart)