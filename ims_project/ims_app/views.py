from django.shortcuts import render, redirect,get_object_or_404
from .forms import (
    CategoryForm,
    SupplierForm,
    ProductForm,
    CustomerForm,
    SalesOrderForm,
    SalesOrderDetailForm,
    PurchaseOrderForm,
    PurchaseOrderDetailForm,
)

from .models import (
    Category,
    Supplier,
    Product,
    Customer,
    SalesOrder,
    SalesOrderDetail,
    PurchaseOrder,
    PurchaseOrderDetail 
)

from django.contrib.auth.decorators import login_required
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.cache import cache_page
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

# Get an instance of the logger
logger = logging.getLogger('custom_logger')



@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, **kwargs):
    cache.delete('all_categories')

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def create_category(request):
    try:

        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                logger.info("Category Data Inserted")
                return redirect('category_detail')  # Redirect to a list view or wherever needed
        else:
            form = CategoryForm()
        return render(request, 'ims/create_category.html', {'form': form})
    

    except Exception as e:
        logger.error(e)
    

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# @cache_page(60 * 15)
# @login_required(login_url='token_obtain_pair')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def category_detail(request):
    try:
        category = Category.objects.all()
        logger.info("Show add Category Data")
        return render(request, 'ims/category_detail.html', {'category': category})
    except Exception as e:
        logger.error(e)


# def category_detail(request):
#     # Check if cached data exists
#     categories = cache.get('all_categories')

#     if not categories:
#         # If not cached, retrieve from the database and cache it
#         categories = Category.objects.all()
#         cache.set('all_categories', categories, timeout=60*15)  # Cache for 15 minutes

#     return render(request, 'ims/category_detail.html', {'category': categories})



@permission_classes([IsAuthenticated])
def category_update(request, pk):
    try:
        category = get_object_or_404(Category, pk=pk)
        if request.method == "POST":
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                logger.info("Category Data Updated Successfullly")
                return redirect('category_detail')
        else:
            form = CategoryForm(instance=category)
        
        return render(request, 'ims/category_update.html', {'form': form, 'category': category})
    except Exception as e:
        logger.error(e)



@permission_classes([IsAuthenticated])
def category_delete(request, pk):
    try:
        category = get_object_or_404(Category, pk=pk)
        if request.method == "POST":
            category.delete()
            logger.info("Category Deleted Successfully")
            return redirect('category_detail')
        
        return render(request, 'ims/category_confirm_delete.html', {'category': category})
    except Exception as e:
        logger.error(e)


def create_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_detail')
    else:
        form = SupplierForm()
    return render(request, 'ims/create_supplier.html', {'form': form})

def supplier_detail(request):
    supplier = Supplier.objects.all()
    return render(request, 'ims/supplier_detail.html', {'supplier': supplier})


# @login_required(login_url='token_obtain_pair')
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_detail')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'ims/supplier_update.html', {'form': form, 'supplier': supplier})


# @login_required(login_url='token_obtain_pair')
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect('supplier_detail')
    
    return render(request, 'ims/supplier_confirm_delete.html', {'supplier': supplier})


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'ims/create_product.html', {'form': form})


def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'ims/create_customer.html', {'form': form})

def create_sales_order(request):
    if request.method == "POST":
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_order_list')
    else:
        form = SalesOrderForm()
    return render(request, 'ims/create_sales_order.html', {'form': form})

def create_sales_order_detail(request):
    if request.method == "POST":
        form = SalesOrderDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_order_detail_list')
    else:
        form = SalesOrderDetailForm()
    return render(request, 'ims/create_sales_order_detail.html', {'form': form})

def create_purchase_order(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'ims/create_purchase_order.html', {'form': form})


def create_purchase_order_detail(request):
    if request.method == "POST":
        form = PurchaseOrderDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_detail_list')
    else:
        form = PurchaseOrderDetailForm()
    return render(request, 'ims/create_purchase_order_detail.html', {'form': form})



# Detail Views




def product_detail(request):
    product = Product.objects.all()
    return render(request, 'ims/product_detail.html', {'product': product})

def customer_detail(request):
    customer = Customer.objects.all()
    return render(request, 'ims/customer_detail.html', {'customer': customer})

def sales_order_detail(request):
    sales_order = SalesOrder.objects.all()
    return render(request, 'ims/sales_order_detail.html', {'sales_order': sales_order})

def sales_order_detail_view(request):
    sales_order_detail = SalesOrderDetail.objects.all()
    return render(request, 'ims/sales_order_detail_view.html', {'sales_order_detail': sales_order_detail})

def purchase_order_detail(request):
    purchase_order = PurchaseOrder.objects.all()
    return render(request, 'ims/purchase_order_detail.html', {'purchase_order': purchase_order})

def purchase_order_detail_view(request):
    purchase_order_detail = PurchaseOrderDetail.objects.all()
    return render(request, 'ims/purchase_order_detail_view.html', {'purchase_order_detail': purchase_order_detail})

