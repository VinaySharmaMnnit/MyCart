from django.contrib import admin
from .models import Product,OrderUpdate,Order,OrderItems,Customer,Shippingaddress,Contact
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderUpdate)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Shippingaddress)
admin.site.register(Contact)