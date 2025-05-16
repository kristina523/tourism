from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField("ФИО", max_length=100, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

# Страны
class Country(models.Model):
    country_name = models.CharField("Название страны", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)
    visa_requirements = models.TextField("Визовые требования", blank=True)

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

# Категории туров
class Category(models.Model):
    category_name = models.CharField("Название категории", max_length=50, unique=True)
    description = models.TextField("Описание", blank=True)
    image_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Туры
class Tour(models.Model):
    title = models.CharField("Название тура", max_length=100)
    description = models.TextField("Описание")
    country = models.ForeignKey(Country, verbose_name="Страна", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    duration_days = models.IntegerField("Длительность (дней)")
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    max_participants = models.IntegerField("Максимум участников", null=True, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    is_hot = models.BooleanField("Горящий тур", default=False)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

# Бронирования
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    booking_date = models.DateTimeField("Дата бронирования", auto_now_add=True)
    participants = models.IntegerField("Количество участников", default=1)
    total_price = models.DecimalField("Общая стоимость", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField("Заметки", blank=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

# Отзывы
class Review(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    rating = models.IntegerField("Оценка")
    comment = models.TextField("Комментарий", blank=True)
    review_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tour')
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

# Платежи
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]
    booking = models.ForeignKey(Booking, verbose_name="Бронирование", on_delete=models.CASCADE)
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField("Дата платежа", auto_now_add=True)
    payment_method = models.CharField("Способ оплаты", max_length=50)
    transaction_id = models.CharField("ID транзакции", max_length=100, blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

# Корзина
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    added_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    participants = models.IntegerField("Количество участников", default=1)
    start_date = models.DateField("Дата начала", null=True, blank=True)
    end_date = models.DateField("Дата окончания", null=True, blank=True)
    price_per_person = models.DecimalField("Цена за человека", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("Общая стоимость", max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'tour', 'start_date')
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьер'),
        ('post', 'Почта'),
    ]
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    delivery_method = models.CharField("Способ доставки", max_length=20, choices=DELIVERY_CHOICES)
    address = models.CharField("Адрес", max_length=255, blank=True)
    is_paid = models.BooleanField("Оплачен", default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} от {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def get_cost(self):
        return self.price * self.quantity