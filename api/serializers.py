from dataclasses import fields
from itertools import product
from pyexpat import model

from rest_framework import serializers
from .models import Product, Order, OrderItem,User
from api.models import Order, Product

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
         data = super().validate(attrs)
         access_token = self.get_token(self.user).access_token
         data["expires_in"] = access_token["exp"] - access_token["iat"]
         data["expires_at"] = access_token["exp"]
         return data
class MyRefreshTokenObtainPairSerializer(TokenRefreshSerializer):
        def validate(self, attrs):
            data = super().validate(attrs)
            access_token = AccessToken(data["access"])
            data["expires_in"] = access_token["exp"] - access_token["iat"]
            data["expires_at"] = access_token["exp"]
            return data
class ProductSerializer(serializers.ModelSerializer):
      class Meta:
          model  = Product
          fields = ('id','name','description','price','stock')
      
      def validate_price(self,value):
           if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
           return value
class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_name=serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(max_digits=10,decimal_places=2,source='product.price')
    class Meta:
        model = OrderItem
        fields = ['quantity', 'item_subtotal','product','product_name','product_price']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name']
                
class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    user =  UserSerializer(read_only=True)
    total_orders=serializers.SerializerMethodField(method_name="total_order")
    order_name=serializers.CharField(source='__str__', read_only=True)
    user_string=serializers.StringRelatedField(source='user') #default username 
    # total_orders=serializers.SerializerMethodField()
    
    # def get_total_orders(self,object):
    #     order_items = object.items.all()
    #     return sum(single_item.item_subtotal for single_item in order_items)
    def total_order(self,object):
            order_items = object.items.all()
            return sum(single_item.item_subtotal for single_item in order_items) 
    class Meta:
            model  = Order
            fields = ('order_id','order_name','user','status','items','total_orders','user_string')

class ProductInforSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField(allow_null=True)

class OrderItemSerializer(serializers.ModelSerializer):
       product=ProductSerializer(read_only=True)
       class Meta:
           model  = OrderItem
           fields = ('quantity','item_subtotal','product','order')                     