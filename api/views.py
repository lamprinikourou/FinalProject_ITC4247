from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
