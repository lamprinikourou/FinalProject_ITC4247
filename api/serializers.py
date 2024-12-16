from rest_framework import serializers
from .models import User, Product, Order
from django.utils.safestring import mark_safe
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = mark_safe(instance.username)
        return representation
 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
 
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'