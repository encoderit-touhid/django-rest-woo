from django.urls import path
from . import views
from . import class_views
from . import api_views

urlpatterns = [
    path('products/',views.product_list),
    path('products/<int:pk>',views.product_details),
    path('orders/',views.order_list),
    path('product-info/',views.product_information),
    path('order-items/',views.order_items),
    
    ### Class View
    path('products-by-class/',class_views.ProductList.as_view(),name="products-by-class"),
    path('products-details-by-class/<int:pk>',class_views.ProductDetails.as_view(),name="products-details-by-class"),
    path('order-by-class/',class_views.OrderList.as_view(),name="orders-by-class"),
    
    path('order-by-class-user/',class_views.UserOrderList.as_view(),name="user-orders"),
    
    ### API view
    path('orders-api-view/',api_views.OrderAPIView.as_view(), name="orders-by-api-view"),
    path('product-create-by-class/',class_views.ProductCreatAPIview.as_view(),name="products-create-by-class"),
    
    ## Single API GET and POST
    path('product-view-create-by-class/',class_views.ProductListCreatAPIview.as_view(),name="product-view-create-by-class"),
    
    
    path('product-details-curd-by-class-id/<int:pk>',class_views.ProductRetrieveUpdateDestroy.as_view(),name="product-details-curd-by-class-id"),
]
