from django.contrib import admin
from .models import Order,OrderDetail,OrderState
#-------------------------------------------------------------------------------

class OrderDetailInLine(admin.TabularInline):
    model= OrderDetail
    extera= 3

@admin.register(Order)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display= ['customer','order_state', 'register_date', 'is_finally', 'discount']
    inlines= [OrderDetailInLine] 
    
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display=['id','order_state_title']