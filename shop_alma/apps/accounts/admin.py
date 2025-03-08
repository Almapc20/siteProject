from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCretionForm
from .models import CustomUser,Customer

class CustomUserAdmin(UserAdmin):
    form= UserChangeForm
    add_form= UserCretionForm
    
    list_display=('mobile_number', 'email', 'name', 'family', 'gender', 'is_admin', 'is_active')    

    list_filter=('is_admin', 'is_active')
    
    fieldsets=(
        (None, {'fields':('mobile_number', 'password')}),
        ('personal info',{ 'fields': ('email', 'name', 'family', 'gender')}),
        ('permissions', {'fields':('is_admin', 'is_active','is_superuser','groups','user_permissions')})
    )
    
    add_fieldsets=(
         (None, {'fields':('mobile_number','email', 'name', 'family', 'gender', 'password1', 'password2')}),
    )
    
    search_fields=('mobile_number',)
    ordering=('mobile_number',)
    
    filter_horizontal=('groups','user_permissions')
    
admin.site.register(CustomUser, CustomUserAdmin)

#--------------------------------------------------------------------------------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','phone_number',]