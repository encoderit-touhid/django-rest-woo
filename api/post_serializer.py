from dataclasses import fields
from itertools import product
from pyexpat import model

from rest_framework import serializers
from .models import Product, Order, OrderItem,User
from api.models import Order, Product


class ProductPostSerializer(serializers.ModelSerializer):
      class Meta:
          model  = Product
          fields = ('name','description','price','stock')