from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shopplyapp.application.commands.commands import CreateOrderCommand
from shopplyapp.application.helpers.mixins import PermissionPolicyMixin, MultiSerializerViewSetMixin
from shopplyapp.adapters.out.db.models import Product, Order, Stock
from shopplyapp.application.helpers.permissions import IsOrdersOwner
from shopplyapp.adapters.into.web.serializers import UserSerializer, GroupSerializer, ProductSerializer, \
    OrderSerializer, StockSerializer, OrderReadSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class ProductViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be listed, viewed or edited
    """
    permission_classes_per_method = {
        "create": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "destroy": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "update": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "partial_update": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "list": [permissions.IsAuthenticatedOrReadOnly],
        "retrieve": [permissions.IsAuthenticatedOrReadOnly]
    }

    queryset = Product.objects.all().order_by('-price')
    serializer_class = ProductSerializer

class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products Stock to be listed, viewed or edited
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    queryset = Stock.objects.all().order_by('-product_id')
    serializer_class = StockSerializer

class OrderViewSet(PermissionPolicyMixin,
                   MultiSerializerViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    serializer_action_classes = {
        'list': OrderReadSerializer,
        'retrieve': OrderReadSerializer,
    }
    permission_classes = [permissions.IsAuthenticated, IsOrdersOwner | permissions.IsAdminUser]
    permission_classes_per_method = {
        "create": [permissions.IsAuthenticated, permissions.IsAdminUser],
        # "update": [permissions.IsAuthenticated, IsOrdersOwner | permissions.IsAdminUser],
        # "partial_update": [permissions.IsAuthenticated, IsOrdersOwner | permissions.IsAdminUser],
        "list": [permissions.IsAuthenticated, IsOrdersOwner | permissions.IsAdminUser],
        "retrieve": [permissions.IsAuthenticated, IsOrdersOwner | permissions.IsAdminUser]
    }

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CreateOrderCommand.execute(serializer, customer=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

