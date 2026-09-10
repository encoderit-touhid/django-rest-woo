from django.http import JsonResponse
from api.models import Order, Product
from api.serializers import ProductSerializer,OrderSerializer,ProductInforSerializer,OrderItem,OrderItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Max
from rest_framework.views import APIView



class OrderAPIView(APIView):
    
    def get(self,request): 
        Orders =Order.objects.prefetch_related('items','items__product','user').all()
        serializer = OrderSerializer(Orders,many=True)
        return Response({
            'success':True,
            'data':serializer.data
        },status.HTTP_200_OK)
