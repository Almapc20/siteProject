from django.contrib import admin
from .models import Order,OrderDetail
#-------------------------------------------------------------------------------

class OrderDetailInLine(admin.TabularInline):
    model= OrderDetail
    extera= 3

@admin.register(Order)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display= ['customer', 'register_date', 'is_finally', 'discount']
    inlines= [OrderDetailInLine] 