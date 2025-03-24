from django.contrib import admin
from .models import Warehouse, WarehousesType

#====================================================================================
@admin.register(WarehousesType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['id', 'warehouses_type_title']
    
#------------------------------------------------------------------------------------    
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['product','price','qty','warehouse_type','register_date']
    
#------------------------------------------------------------------------------------    
