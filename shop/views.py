from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, OrderItem
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    messages.success(request, f'Добавлено {product.name} в корзину.')
    return redirect('shop:product_list')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # Простейшая обработка изменения количества
        for item in cart_items:
            quantity_str = request.POST.get(f'quantity_{item.id}')
            if quantity_str and quantity_str.isdigit():
                qty = int(quantity_str)
                if qty > 0:
                    item.quantity = qty
                    item.save()
                else:
                    item.delete()
        return redirect('shop:cart_detail')

    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_create(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if order.delivery_type == 'pickup':
                order.address = ''
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
            cart_items.delete()  # Очистка корзины после заказа
            messages.success(request, f'Заказ #{order.id} успешно создан')
            return redirect('shop:product_list')
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'form': form})