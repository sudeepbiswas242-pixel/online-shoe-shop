
from django.contrib.auth.models import User

from .models import Shoe, Order


def admin_statistics(request):

    total_shoes = Shoe.objects.count()

    total_orders = Order.objects.count()

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    total_sales = sum(
        order.total_amount
        for order in Order.objects.all()
        if order.status != 'cancelled'
    )

    return {
        'admin_total_shoes': total_shoes,
        'admin_total_orders': total_orders,
        'admin_total_customers': total_customers,
        'admin_total_sales': total_sales,
    }

