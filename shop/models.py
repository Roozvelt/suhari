from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_piece = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='products/')
    packaging_size = models.PositiveIntegerField(default=1, help_text='Кол-во штук в одной упаковке')

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, help_text='Кол-во упаковок')

    def get_total_price(self):
        return self.product.price_per_piece * self.product.packaging_size * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity} упаковок'

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз со склада'),
    ]
    PAYMENT_CHOICES = [
        ('prepay', 'Предоплата на сайте'),
        ('cod', 'Оплата при получении'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    address = models.CharField(max_length=255, blank=True)  # адрес нужен если доставка
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # упаковки

    def get_total_price(self):
        return self.product.price_per_piece * self.product.packaging_size * self.quantity