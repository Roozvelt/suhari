from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from yookassa import Configuration

from .forms import OrderCreateForm, OrderStatusUpdateForm
from .models import Product, CartItem, Order, OrderItem

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def get_session_cart(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def save_session_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def transfer_cart(request, user):
    session_cart = get_session_cart(request)
    if session_cart:
        for product_id, quantity in session_cart.items():
            product = get_object_or_404(Product, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        request.session['cart'] = {}
        save_session_cart(request, {})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 0))

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    else:
        cart = get_session_cart(request)
        product_id = str(product.id)
        cart[product_id] = cart.get(product_id, 0) + quantity
        save_session_cart(request, cart)

    messages.success(request, f'Добавлено {product.name} в корзину.')
    return redirect('shop:product_list')


@login_required
def item_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product=product).delete()
    else:
        cart = get_session_cart(request)
        product_id = str(product.id)
        if product_id in cart:
            del cart[product_id]
            save_session_cart(request, cart)

    messages.success(request, f'{product.name} удалён из корзины.')
    return redirect('shop:cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.get_total_price() for item in cart_items)
    else:
        cart = get_session_cart(request)
        cart_items = []
        total_price = 0
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'get_total_price': product.price * quantity
                })
                total_price += product.price * quantity
            except Product.DoesNotExist:
                continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'auth_required': not request.user.is_authenticated
    }
    return render(request, 'shop/cart_detail.html', context)


@login_required
def order_create(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order_price = 0
            order = form.save(commit=False)
            order.user = request.user
            if order.delivery_type == 'pickup':
                order.address = ''
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                order_price += item.get_total_price()
            order.total_price = order_price
            order.save()
            if order.payment_type == 'card':
                return render(request, 'shop/order_pay.html', {'order': order, 'form': form})
            cart_items.delete()  # Очистка корзины после заказа
            messages.success(request, f'Заказ #{order.id} успешно создан')
            return redirect('shop:product_list')
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'form': form})


@login_required
def orders_list(request):
    user = request.user
    if user.is_staff:
        orders = Order.objects.order_by('-created_at')
        return render(request, 'shop/admin/orders_list.html', {'orders': orders})
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'shop/user/orders_list.html', {'orders': orders, 'is_admin': False})


@login_required
def order_detail(request, pk):
    user = request.user
    if user.is_staff:
        order = get_object_or_404(Order, pk=pk)
        if request.method == 'POST':
            form = OrderStatusUpdateForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('shop:orders')
        else:
            form = OrderStatusUpdateForm(instance=order)
        return render(request, 'shop/admin/order_detail.html', {'order': order, 'form': form})
    else:
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'shop/user/order_detail.html', {'order': order, 'is_admin': False})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'new':
        order.status = 'canceled'
        order.save()
    return redirect('shop:orders')
