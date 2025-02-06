from django.contrib import admin
from .models import *

admin.site.register(Debtor) 
admin.site.register(Debt)
admin.site.register(Product)
admin.site.register(ProductRequest)
admin.site.register(Warehouse)