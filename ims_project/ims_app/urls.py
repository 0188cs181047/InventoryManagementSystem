from django.urls import path
from . import views


urlpatterns = [
    path('category/create/', views.create_category, name='create_category'),
    path('supplier/create/', views.create_supplier, name='create_supplier'),
    path('product/create/', views.create_product, name='create_product'),
    path('customer/create/', views.create_customer, name='create_customer'),
    path('sales_order/create/', views.create_sales_order, name='create_sales_order'),
    path('sales_order_detail/create/', views.create_sales_order_detail, name='create_sales_order_detail'),
    path('purchase_order/create/', views.create_purchase_order, name='create_purchase_order'),
    path('purchase_order_detail/create/', views.create_purchase_order_detail, name='create_purchase_order_detail'),
    path('category/details/', views.category_detail, name='category_detail'),
    path('supplier/details/', views.supplier_detail, name='supplier_detail'),
    path('product/details/', views.product_detail, name='product_detail'),
    path('customer/details/', views.customer_detail, name='customer_detail'),
    path('sales_order/details/', views.sales_order_detail, name='sales_order_detail'),
    path('sales_order_detail/details/', views.sales_order_detail_view, name='sales_order_detail_view'),
    path('purchase_order/details/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase_order_detail/details/', views.purchase_order_detail_view, name='purchase_order_detail_view'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('supplier/update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('supplier/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
]
