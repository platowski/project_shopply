from shopplyapp.models import Product
from shopplyapp.serializers import OrderSerializer, ProductSerializer


class CreateOrderCommand:
    @staticmethod
    def execute(serializer: OrderSerializer, customer):
        serializer.get_attribute()
        serializer.save(customer=customer)
