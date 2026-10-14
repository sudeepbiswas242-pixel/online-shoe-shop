
from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'add-to-cart/<int:shoe_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),
    path(
    'payment-success/',
    views.payment_success,
    name='payment_success'
),

    path(
        'remove-from-cart/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'update-cart/<int:item_id>/<str:action>/',
        views.update_cart_quantity,
        name='update_cart_quantity'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),
     
path(
    'my-orders/',
    views.my_orders,
    name='my_orders'
),

path('about/', views.about, name='about'),




]

