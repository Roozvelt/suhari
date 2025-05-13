from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='products/')
    weight = models.PositiveIntegerField(default=200, help_text='вес товара')

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, help_text='Количество')

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity} упаковок'

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз со склада'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В работе'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменён'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    address = models.CharField(max_length=255, blank=True)  # адрес нужен если доставка
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_id = models.CharField(max_length=100, blank=True)  # ID платежа в ЮKassa
    payment_type = models.CharField(
        max_length=50,
        choices=[('card', 'Оплата картой онлайн'), ('cash', 'Наличные при получении')],
        default='card'
    )
    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} — {self.get_status_display()}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # упаковки
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total_price(self):
        return self.product.price * self.quantity