from itertools import product
from re import search

from django.http import JsonResponse
from api.views import order_items
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Order, Product
from api.serializers import ProductSerializer,OrderSerializer,ProductInforSerializer,OrderItem,OrderItemSerializer,OrderViewSetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Max
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from api.post_serializer import ProductPostSerializer
from api.filters import ProductFilter, InStockProductFilterBackend,ProductPagination,OrderFilter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
from .serializers import MyTokenObtainPairSerializer, MyRefreshTokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer
from .post_serializer import OrderCreateSerializer
from api.permissions import IsSelfOrder

class OrderListViewSet(viewsets.ModelViewSet): #auto Get Method
    queryset = Order.objects.prefetch_related('items','items__product','user').all()
    serializer_class = OrderViewSetSerializer
    permission_classes=[IsAuthenticated]
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        query=super().get_queryset()
        if not self.request.user.is_staff:
            return query.filter(user=self.request.user)
        return query       
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()
        
    @action(detail=False, methods=['get'],permission_classes=[IsAuthenticated],url_path='user-order')
    def get_user_order(self, request):
        orders=self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['PUT'],permission_classes=[IsAdminUser|IsSelfOrder],url_path='update-single-order-status-only')
    def update_single_order_status_only(self, request, pk=None):
            order = self.get_object()
            new_status = request.data.get('status')
            valid_statuses = dict(Order.StatusChoices.choices)
            if new_status not in valid_statuses:
                return Response({'status': f'Invalid status. Must be one of {list(valid_statuses)}'},status=status.HTTP_400_BAD_REQUEST)
            order.status = new_status
            order.save(update_fields=['status'])
            serializer = self.get_serializer(order)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    @action(detail=False,methods=['get'],permission_classes=[AllowAny],url_path='test/(?P<id>[0-9]+)/(?P<name>[^/.]+)')
    def test_id_name(self, request, id, name):
        return Response({
            'id': id,
            'name': name
            },status=status.HTTP_200_OK)