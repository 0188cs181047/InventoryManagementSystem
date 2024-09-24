from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.supplier_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name



class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customer_name


class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.customer_name}"


class SalesOrderDetail(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} in Order #{self.order.id}"


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase Order #{self.id} - {self.supplier.supplier_name}"


class PurchaseOrderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='purchase_order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} in Purchase Order #{self.purchase_order.id}"


