from decimal import Decimal
from .models import Tour

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, tour, quantity=1, reload=False):
        tour_id = str(tour.id)
        if tour_id not in self.cart:
            self.cart[tour_id] = {'quantity': 0, 'price': str(tour.price)}
        if reload:
            self.cart[tour_id]['quantity'] = quantity
        else:
            self.cart[tour_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, tour):
        tour_id = str(tour.id)
        if tour_id in self.cart:
            del self.cart[tour_id]
            self.save()

    def __iter__(self):
        tour_ids = self.cart.keys()
        tours = Tour.objects.filter(id__in=tour_ids)
        for tour in tours:
            cart_item = self.cart[str(tour.id)]
            cart_item['tour'] = tour
            cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.save()