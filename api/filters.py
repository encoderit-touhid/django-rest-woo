from rest_framework import filters
import django_filters 
from .models import Order, Product
from rest_framework.pagination import PageNumberPagination

class InStockProductFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductPagination(PageNumberPagination):
    page_size = 2
    page_query_param='page_num'
    page_size_query_param='size'
    max_page_size=6

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # fields = ['name','description','price']
        fields = {
            'name':['exact','contains'],
            'price':['range','gt','lt','exact']
        }
        
        
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        # fields = ['status','user__name','user__first_name']
        fields = {
            'status':['exact'],
            'created_at':['range','gt','lt','exact']
        }        
        