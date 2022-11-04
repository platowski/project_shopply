from django.contrib.auth.models import User, Group
from rest_framework import serializers

from shopplyapp.adapters.out.db.models import Product, Order, Stock, ProductBatch


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class StockSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Stock
        fields = ['quantity', 'product']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # no idea why this is not being listed @todo
    product_quantity = serializers.ReadOnlyField(source='stock.quantity', read_only=True)

    class Meta:
        model = Product
        fields = ['url', 'name', 'product_quantity', 'price', 'id']


class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)
    product_name = serializers.ReadOnlyField(source='sku.product.name')
    class Meta:
        model = ProductBatch
        fields = ['quantity', 'product_name']


class OrderReadSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    status = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['url', 'created_at', 'status', 'total', 'customer_name', 'items']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    status = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    quantity = serializers.IntegerField()
    # @todo figure out how to work with hyperlinkedRelatedField
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['url', 'created_at', 'status', 'total', 'customer_name', 'product', 'quantity']

