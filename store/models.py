
from django.db import models
from django.contrib.auth.models import User


class Shoe(models.Model):

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100,
        choices=[ ('sneakers', 'Sneakers'), ('running', 'Running Shoes'), ('formal', 'Formal Shoes'), ('boots', 'Boots'), ('sandals', 'Sandals'), ('kids', 'Kids Shoes'), ],
        default='sneakers'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='shoes/',
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name


class CartItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.user.username} - {self.shoe.name}"


class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()


    # ==========================
    # ORDER STATUS
    # ==========================

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )


    # ==========================
    # PAYMENT METHOD
    # ==========================

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Card / Online Payment'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cod'
    )


    # ==========================
    # ORDER TOTAL
    # ==========================

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    # ==========================
    # RAZORPAY PAYMENT DETAILS
    # ==========================

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    # ==========================
    # ORDER DATE
    # ==========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.shoe.name} x {self.quantity}"

