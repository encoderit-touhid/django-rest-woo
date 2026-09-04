from dataclasses import fields
from pyexpat import model

from rest_framework import serializers
from .models import Product, Order, OrderItem

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
    class Meta:
        model = OrderItem
        fields = ['quantity', 'item_subtotal','product']
        
class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    
    class Meta:
            model  = Order
            fields = ('order_id','user','status','items')       