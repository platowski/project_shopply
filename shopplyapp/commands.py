from shopplyapp.models import Product
from shopplyapp.serializers import OrderSerializer, ProductSerializer


class CreateOrderCommand:
    @staticmethod
    def execute(serializer: OrderSerializer, customer):

        serializer.save(customer=customer)
