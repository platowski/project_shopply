from django.db import transaction
from shopplyapp.adapters.into.web.serializers import OrderSerializer, OrderReadSerializer
from shopplyapp.adapters.out.db.models import ProductBatch, Stock, Order
from shopplyapp.application.helpers.exceptions import OutOfStockException


class CreateOrderCommand:
    @classmethod
    def execute(cls, serializer: OrderSerializer, customer):
        product_id = int(serializer.initial_data["product"])
        quantity = int(serializer.initial_data["quantity"])
        sku = cls.get_stock_unit(product_id=product_id)
        cls.validate_product_availability(sku, int(quantity))
        total = sku.product.price * quantity
        # It is super simple approach to avoid race condition when multiple users want to buy last item
        # It requires async vacuum that will be fired up each n minutes to cancel unpaid orders older than X
        # Cancelling order will release quantity (product.quantity += ... )

        order = Order(customer_id=customer.id, total=total)
        # @todo verify transaction isolation level (at least read-commited)!
        with transaction.atomic():
            order.save()
            batch = ProductBatch(sku=sku, quantity=int(quantity), order_id=order.id)
            batch.save()
            sku.quantity -= quantity
            sku.save()
        return order.id

    @staticmethod
    def get_stock_unit(product_id: int) -> Stock:
        return Stock.objects.get(product_id=product_id)

    @staticmethod
    def validate_product_availability(sku: Stock, order_quantity: int):
        if sku.quantity < order_quantity:
            raise OutOfStockException(
                "Sorry, we don't have enough quantity of {}".format(sku.product.name)
            )
