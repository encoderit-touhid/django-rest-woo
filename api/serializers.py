from dataclasses import fields
from itertools import product
from pyexpat import model

from rest_framework import serializers
from .models import Product, Order, OrderItem,User

class ProductSerializer(serializers.ModelSerializer):
      class Meta:
          model  = Product
          fields = ('name','description','price','stock')
      
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
    user_string=serializers.StringRelatedField(source='user')
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