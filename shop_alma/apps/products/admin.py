from django.contrib import admin
from .models import Brand, Product, ProductGallery, ProductGroup, ProductFeature, Feature
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field

#-------------------برند ها-----------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display= ('brand_title','slug', )
    list_filter= ('brand_title',)
    search_fields= ('brand_title',)
    ordering= ('brand_title',)
    
# -------------------------- گروه کالا ------------------------------------------------------------
# ================================================================================================
#------------------زیرگروه های گروه کالاها -------------------------------------------------------------
class ProductGroupInstancelineAdmin(admin.TabularInline):
    model= ProductGroup
    extra=0
#----------------------- ویرایش داده ها -----------------------------------------------------------
def de_active_product_group(modeladmin, request, queryset):
    res= queryset.update(is_active= False)
    message= f'تعداد {res} گروه  کالا غیر فعال شد'
    modeladmin.message_user(request, message)

def active_product_group(modeladmin, request, queryset):
    res= queryset.update(is_active= True)
    message= f'تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request, message)
    
def export_json(modeladmin, request, queryset):
    response= HttpResponse(content_type= 'application/json')
    serializers.serialize("json", queryset, stream= response)
    return response

#---------------------------------کاستوم کردن فیلتر گروه ها در ادمین----------------------------------------------
class GroupFilter(SimpleListFilter):
    title= 'گروه محصولات'
    parameter_name= 'group'
    
    def lookups(self, request, model_admin):
        sub_groups= ProductGroup.objects.filter(~Q(group_parent=None))
        groups= set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title,) for item in groups]
    # --------------------- برای اینکه دکمه همه در فیلتر کار کند  ------------------------------------
    def queryset(self, request, queryset):
        if self.value()!= None:
            return queryset.filter(Q(group_parent= self.value()))
        return queryset
            
#-------------------------------------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display= ('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group')
    list_filter= ('group_title', ('group_parent', DropdownFilter), 'is_active')
    search_fields= ('group_title',)
    ordering= ('group_parent','group_title',)
    inlines= [ProductGroupInstancelineAdmin]
    actions= [de_active_product_group, active_product_group, export_json, ]    
    list_editable= ['is_active',]
    
    # -------------- add colom -------------------------------------------------------------------------------
    def get_queryset(self, *args, **kwargs):
        qs= super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)   
        qs= qs.annotate(sub_group= Count('groups'))    
        qs= qs.annotate(produc_of_group= Count('products_of_groups'))    
        return qs

    @short_description('تعداد زیرگروه ها')
    @order_field('sub_group')
    def count_sub_group(self, obj):
        return obj.sub_group

    # ------------------------- کاستوم کردن فیلتر گروه ها در توسط دکوریتورها به جای دستور قبل در ادمین-------------------------------------------
    @short_description('تعداد کالاهای گروه')
    @order_field('produc_of_group')
    def count_produc_of_group(self, obj):
        return obj.produc_of_group
    
    # ------------------------- نمایش فارسی لیست منو ------------------------------------------
    # count_sub_group.short_description= "تعداد زیرگروه ها"
    de_active_product_group.short_description= "غیر فعال کردن گروه های انتخاب شده"        
    active_product_group.short_description= " فعال کردن گروه های انتخاب شده"        
    export_json.short_description= "  از گروه های انتخاب شده json خروجی"
    
    
#--------------------------چیدمان فرم گروهبندی کالا در ادمین----------------------------------------------------------
    fieldsets = (
        ("اطلاعات گروه کالا", {"fields": (
            ('group_title', 'slug', ),
            'image_name',
            ('group_parent', 'is_active', ),
            'description',
                            
            ),
        }),
        
        ("تاریخ و زمان", {"fields": (
            'published_date',
            ),
        }),
    )

#------------------------------------------------------------------------------------

# -------------------------- ویژگی ها ------------------------------------------------------------
# ================================================================================================
# --------------------------ویژگی محصولات ------------------------------------------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display= ('feature_name',)
    list_filter= ('feature_name',)
    search_fields= ('feature_name',)
    ordering= ('feature_name',)
    
# -------------------------- محصولات ------------------------------------------------------------
# ================================================================================================
#-----------------فعال و غیر فعال کردن کالا-------------------------------------------------------------------
def de_active_product(modeladmin, request, queryset):
    res= queryset.update(is_active= False)
    message= f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

def active_product(modeladmin, request, queryset):
    res= queryset.update(is_active= True)
    message= f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)

# --------------------------------------ویژگی ها -------------------------------------------------------------------
class ProductFeatureInlineAdmin(admin.TabularInline):
    model= ProductFeature
    extra=2
# ---------------------------- گالری تصاویر در صفحه جِزِئیات-----------------------------------------------------------------------------
class ProductGalleryInlineAdmin(admin.TabularInline):
    model= ProductGallery
    extra=3
# ---------------------------------------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  
    list_display= ('product_name','price','brand','is_active','update_date','slug',)
    list_filter= ('brand','product_group')
    search_fields= ('product_name',)
    ordering= ('update_date','product_name',)
    actions=[de_active_product, active_product,]
    inlines= [ProductFeatureInlineAdmin, ProductGalleryInlineAdmin, ]
    list_editable= ['is_active',]
    
    de_active_product.short_description= "غیر فعال کردن کالاهای انتخاب شده"        
    active_product.short_description= " فعال کردن کالاهای انتخاب شده"        
    # display_product_group.short_description= "گروه های کالا" 

      
    def display_product_group(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
       
    de_active_product.short_description= "غیر فعال کردن کالاهای انتخاب شده"        
    active_product.short_description= " فعال کردن کالاهای انتخاب شده"        
    display_product_group.short_description= "گروه های کالا"        
   
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name== 'product_group':
            kwargs["queryset"]= ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# ---------------------------------------------------------------------------------------------------------
#--------------------------چیدمان فرم کالا در ادمین----------------------------------------------------------
    fieldsets = (
        ("اطلاعات محصول", {"fields": (
            'product_name', 'price',
            'image_name',
            ('brand', 'product_group', 'is_active', ),
            'description',
            'slug',
                        
            ),
        }),
        
        ("تاریخ و زمان", {"fields": (
            'published_date',
            ),
        }),
    )

#------------------------------------------------------------------------------------
# ================================================================================================