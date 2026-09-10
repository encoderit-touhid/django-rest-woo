from itertools import product

from django.http import JsonResponse
from api.models import Order, Product
from api.serializers import ProductSerializer,OrderSerializer,ProductInforSerializer,OrderItem,OrderItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from api.post_serializer import ProductPostSerializer

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
from .serializers import MyTokenObtainPairSerializer, MyRefreshTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyRefreshTokenObtainPairView(TokenRefreshView):
      serializer_class = MyRefreshTokenObtainPairSerializer  

class ProductList(generics.ListAPIView): #auto Get Method
    #queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    

class ProductDetails(generics.RetrieveAPIView): #auto Get Method
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'pk'

class OrderList(generics.ListAPIView): #auto Get Method
    queryset = Order.objects.prefetch_related('items','items__product','user').all()
    serializer_class = OrderSerializer        

class UserOrderList(generics.ListAPIView): #auto Get Method
    queryset = Order.objects.prefetch_related('items','items__product','user').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] 
    def get_queryset(self):
        user = self.request.user
        query=super().get_queryset()
        return query.filter(user=user)

class ProductCreatAPIview(generics.CreateAPIView):
    model = Product
    serializer_class = ProductPostSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)        

class ProductListCreatAPIview(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        def get_permissions(self):
             self.permission_classes=[AllowAny]
             if self.request.method == 'POST':
                  self.permission_classes=[IsAdminUser]
             return super().get_permissions()        
         

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): #auto Get Method
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'pk'
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ('PUT','DELETE') :
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()
    def delete(self, request, *args, **kwargs):
            self.destroy(request, *args, **kwargs)
            return Response(
                {
                    "message": "Deleted successfully."
                },status=status.HTTP_204_NO_CONTENT
                )           