from django.db import models
from django.contrib.auth.models import User

from shopplyapp.application.helpers.exceptions import OutOfStockException


class Product(models.Model):
    name = models.CharField(max_length=200)
    # single currency i.e. USD
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # description, photos etc

class Stock(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte='0'), name='stock_quantity_non_negative'),
        ]
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='stock',
        unique=True
    )
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        # Yes, this flow is oversimplified
        PENDING_PAYMENT = 'Payment pending'
        PAID = 'Paid'
        IN_DELIVERY = 'Delivery'
        DELIVERED = 'Delivered'
        CANCELLED = 'Cancelled'
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING_PAYMENT,
    )
    # items d.product_barch_set.objects.all() model prepared for multiple order lines, however, api will stick to 1:1
    total = models.DecimalField(max_digits=10, decimal_places=2)


class ProductBatch(models.Model):
    sku = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.RESTRICT)

    class BatchStatus(models.TextChoices):
        RESERVED = 'reserved'
        SOLD = 'sold'
        # released back to stock quantity poll
        RELEASED = 'released'

    status = models.CharField(
        max_length=20,
        choices=BatchStatus.choices,
        default=BatchStatus.RESERVED,
    )