from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.PurchaseOrder)
admin.site.register(models.PurchaseOrderDetail)
admin.site.register(models.SalesOrder)
admin.site.register(models.SalesOrderDetail)
admin.site.register(models.Supplier)
