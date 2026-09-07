from django.http import JsonResponse
from api.models import Order, Product
from api.serializers import ProductSerializer,OrderSerializer,ProductInforSerializer,OrderItem,OrderItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Max
# def product_list(request):
#     products =Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return JsonResponse({
#         'success':True,
#         'data':serializer.data
#     })

@api_view(['GET'])
def product_list(request):
    products =Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response({
        'success':True,
        'data':serializer.data
    },status.HTTP_200_OK)
    
# def product_details(request,pk):
#     product =Product.objects.get(pk=pk)
#     serializer = ProductSerializer(product)
#     return JsonResponse({
#         'success':True,
#         'data':serializer.data
#     }) 

@api_view(['GET'])
def product_details(request,pk):
    product =get_object_or_404(Product,pk=pk)
    serializer = ProductSerializer(product)
    return Response({
                'success':True,
                'data':serializer.data
            },status.HTTP_200_OK)
     
       
# @api_view(['GET'])
# def product_details(request,pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response({
#                 'success':False,
#                 'data':[]
#             },status.HTTP_404_NOT_FOUND)

#     serializer = ProductSerializer(product)
#     return Response({
#             'success':True,
#             'data':serializer.data
#         },status.HTTP_200_OK)

@api_view(['GET'])
def order_list(request):
    Orders =Order.objects.prefetch_related('items','items__product','user').all()
    # Orders =Order.objects.select_related('items','items__product','user').all()
    # for order in Orders:
    #     for product in order.products.all():
    #         print(f"product name {product.name}")
    #         for order in product.orders.all():
    #             print(f"order id {order.order_id}") 
    serializer = OrderSerializer(Orders,many=True)
    return Response({
        'success':True,
        'data':serializer.data
    },status.HTTP_200_OK)

@api_view(['GET'])
def product_information(request):
    products = Product.objects.all()
    product_info_serializer = ProductInforSerializer({
        'products': products,
        'count': products.count(),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'] or 0.0
    })
    return Response({
            'success':True,
            'data':product_info_serializer.data
        },status.HTTP_200_OK)
    
@api_view(['GET'])
def order_items(request):
    order_items = OrderItem.objects.select_related('product').all()
    order_item_serializer = OrderItemSerializer(order_items,many=True)
    return Response({
            'success':True,
            'data':order_item_serializer.data
        },status.HTTP_200_OK)    
    