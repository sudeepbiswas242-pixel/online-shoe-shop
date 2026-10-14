
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import razorpay
from django.conf import settings

from .models import Shoe, CartItem, Order, OrderItem


# Razorpay client
client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)



def home(request):

    category = request.GET.get('category')

    if category:
        shoes = Shoe.objects.filter(
            category=category
        )
    else:
        shoes = Shoe.objects.all()

    categories = Shoe.objects.values_list(
        'category',
        flat=True
    ).distinct()

    cart_count = 0

    if request.user.is_authenticated:

        cart_items = CartItem.objects.filter(
            user=request.user
        )

        cart_count = sum(
            item.quantity
            for item in cart_items
        )

    return render(
        request,
        'home.html',
        {
            'shoes': shoes,
            'categories': categories,
            'selected_category': category,
            'cart_count': cart_count,
        }
    )



def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check password
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        # Check username
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')


def profile(request):

    return render(
        request,
        'profile.html'
    )


def add_to_cart(request, shoe_id):

    if not request.user.is_authenticated:

        return redirect('login')

    shoe = Shoe.objects.get(
        id=shoe_id
    )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        shoe=shoe
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('home')


def cart(request):

    if not request.user.is_authenticated:

        return redirect('login')

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    total = sum(
        item.shoe.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:

        return redirect('login')

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')


def update_cart_quantity(request, item_id, action):

    if not request.user.is_authenticated:

        return redirect('login')

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    if action == 'increase':

        cart_item.quantity += 1

        cart_item.save()

    elif action == 'decrease':

        if cart_item.quantity > 1:

            cart_item.quantity -= 1

            cart_item.save()

        else:

            cart_item.delete()

    return redirect('cart')


def about(request):

    return render(
        request,
        'about.html'
    )



def checkout(request):

    if not request.user.is_authenticated:

        return redirect('login')


    cart_items = CartItem.objects.filter(
        user=request.user
    )


    if not cart_items.exists():

        return redirect('cart')


    total = sum(
        item.shoe.price * item.quantity
        for item in cart_items
    )


    if request.method == 'POST':

        full_name = request.POST['full_name']

        phone = request.POST['phone']

        address = request.POST['address']

        payment_method = request.POST['payment_method']


        # ==================================
        # CASH ON DELIVERY
        # ==================================

        if payment_method == 'cod':

            order = Order.objects.create(

                user=request.user,

                full_name=full_name,

                phone=phone,

                address=address,

                payment_method=payment_method,

                total_amount=total

            )


            for item in cart_items:

                OrderItem.objects.create(

                    order=order,

                    shoe=item.shoe,

                    quantity=item.quantity,

                    price=item.shoe.price

                )


            cart_items.delete()


            return redirect(
                'order_success',
                order_id=order.id
            )


        # ==================================
        # RAZORPAY PAYMENT
        # ==================================

        amount_in_paise = int(
            total * 100
        )


        razorpay_order = client.order.create({

            'amount': amount_in_paise,

            'currency': 'INR',

            'payment_capture': 1

        })


        order = Order.objects.create(

            user=request.user,

            full_name=full_name,

            phone=phone,

            address=address,

            payment_method=payment_method,

            total_amount=total,

            razorpay_order_id=razorpay_order['id']

        )


        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                shoe=item.shoe,

                quantity=item.quantity,

                price=item.shoe.price

            )


        return render(

            request,

            'checkout.html',

            {

                'cart_items': cart_items,

                'total': total,

                
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'razorpay_amount': amount_in_paise,
                'order_id': order.id,


            }

        )


    return render(

        request,

        'checkout.html',

        {

            'cart_items': cart_items,

            'total': total,

        }

    )






def order_success(request, order_id):

    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {
            'order': order,
        }
    )


def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders,
        }
    )

def payment_success(request):

    if request.method == 'POST':

        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            order = Order.objects.get(
                razorpay_order_id=order_id,
                user=request.user
            )

            # Verify Razorpay payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Save payment details
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.status = 'processing'
            order.save()

            # Clear user's cart
            CartItem.objects.filter(
                user=request.user
            ).delete()

            return redirect(
                'order_success',
                order_id=order.id
            )

        except Exception:
            messages.error(
                request,
                'Payment verification failed.'
            )
            return redirect('checkout')

    return redirect('checkout')


