from django.contrib.auth.models import User, Group
from rest_framework import serializers

from shopplyapp.models import Product, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'name', 'quantity', 'price']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    status = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['url', 'created_at', 'status', 'product', 'quantity', 'total', 'customer_name']

