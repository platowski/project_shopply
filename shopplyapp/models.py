from django.db import models
from django.contrib.auth.models import User

from shopplyapp.exceptions import OutOfStockException


class Product(models.Model):
    name = models.CharField(max_length=200)
    # single currency i.e. USD
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #keeping quantity in same model is also oversimplification
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        # Yes, this flow is oversimplified
        CREATED = 'Created'
        PAID = 'Paid'
        IN_DELIVERY = 'Delivery'
        DELIVERED = 'Delivered'
        CANCELLED = 'Cancelled'
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
    )
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # normally, I would create CreateOrderCommand, but DRF seems to be favoring ActiveRecord approach - huge dislike
        if self.product.quantity < self.quantity:
            raise OutOfStockException("Sorry, we don't have enough quantity of {}".format(self.product.name))

        self.total = self.product.price * self.quantity

        product = Product.objects.get(id=self.product.id)
        # It is super simple approach to avoid race condition when multiple users want to buy last item
        # It requires async vacuum that will be fired up each n minutes to cancel unpaid orders older than X
        # Cancelling order will release quantity (product.quantity += ... )
        # of course this should be modelled by entities like Stock and ProductBatchLock, because it won't scale
        # and maintenance would be a horror,
        # but I tried to fit in given timeframe


        # this won't work! save() has to be idempotent looking for another solution
        product.quantity -= self.quantity

        # this should be a transaction!
        product.save()

        return super(Order, self).save(*args, **kwargs)
        # here transaction should be commited or rolled back