from dataclasses import fields
from itertools import product
from pyexpat import model
from pickle import TRUE
from rest_framework import serializers
from .models import Product, Order, OrderItem,User
from api.models import Order, Product
from django.db import transaction

class ProductPostSerializer(serializers.ModelSerializer):
      class Meta:
          model  = Product
          fields = ('name','description','price','stock')


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
       class Meta:
            model = OrderItem
            fields = ('product', 'quantity')
    
    order_id = serializers.UUIDField(read_only=TRUE)
    order_name=serializers.CharField(source='__str__', read_only=True)
    items = OrderItemCreateSerializer(many=True,required=False)
    
    def create(self, validated_data):
        item_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in item_data:
                OrderItem.objects.create(order=order, **item)
        return order
    
    def update(self, instance, validated_data):
        item_data = validated_data.pop('items', None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            # if item_data is not None:
            #     existing_items = {item.product_id: item for item in instance.items.all()}
            #     seen_product_ids = set()

            #     for item in item_data:
            #         product = item['product']
            #         quantity = item['quantity']
            #         seen_product_ids.add(product.id)

            #         existing_item = existing_items.get(product.id)
            #         if existing_item is not None:
            #             existing_item.quantity = quantity
            #             existing_item.save(update_fields=['quantity'])
            #         else:
            #             OrderItem.objects.create(order=instance, product=product, quantity=quantity)

            #     for product_id, existing_item in existing_items.items():
            #         if product_id not in seen_product_ids:
            #             existing_item.delete()
            if item_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                # Recreate items with the updated data
                for item in item_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance
        
        
    class Meta:
     model  = Order
     fields = ('order_id','status','items','order_name','user')
     extra_kwargs = {
            'user': {'read_only': True}
        }      


          