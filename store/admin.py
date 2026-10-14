
from django.contrib import admin

from .models import Shoe, CartItem, Order, OrderItem


# ==========================================
# SHOE ADMIN
# ==========================================

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'stock',
    )

    search_fields = (
        'name',
        'category',
        'description',
    )

    list_filter = (
        'category',
    )

    list_editable = (
        'price',
        'stock',
    )

    ordering = (
        'name',
    )




# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'total_amount',
        'payment_method',
        'status',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'user__username',
    )

    list_filter = (
        'payment_method',
        'status',
        'created_at',
    )

    list_editable = (
        'status',
    )

    ordering = (
        '-created_at',
    )


# ==========================================
# ORDER ITEM ADMIN
# ==========================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'shoe',
        'quantity',
        'price',
    )

    search_fields = (
        'shoe__name',
        'order__id',
    )

    list_filter = (
        'shoe',
    )


# ==========================================
# ADMIN PANEL BRANDING
# ==========================================

admin.site.site_header = "👟 ShoeStore Administration"

admin.site.site_title = "ShoeStore Admin"

admin.site.index_title = "Welcome to ShoeStore Admin Panel"

