from django import forms
from .models import Category, Supplier, Product, Customer, SalesOrder, SalesOrderDetail, PurchaseOrder, PurchaseOrderDetail

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_name', 'phone_number', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'supplier', 'quantity_in_stock', 'reorder_level', 'price', 'description']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'email', 'phone_number', 'address']


class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'status', 'total_amount']


class SalesOrderDetailForm(forms.ModelForm):
    class Meta:
        model = SalesOrderDetail
        fields = ['order', 'product', 'quantity', 'price', 'total']


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'status', 'total_amount']


class PurchaseOrderDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderDetail
        fields = ['purchase_order', 'product', 'quantity', 'price', 'total']
