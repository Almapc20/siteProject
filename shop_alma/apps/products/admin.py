from django.db.models.fields import Field
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from .models import Brand, ProductGroup, Product, ProductFeature, Feature, ProductGallery, FeatureValue
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models.aggregates import Count
from django.core import serializers
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field

#-------------------برند ها-----------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display= ('brand_title','slug', )
    list_filter= ('brand_title',)
    search_fields= ('brand_title',)
    ordering= ('brand_title',)
    
#--------------------فعال و غیر فعال کردن گروه ----------------------------------------------------------------
def de_active_product_group(modeladmin, request, queryset):
    res= queryset.update(is_active= False)
    message= f'تعداد گروه {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

def active_product_group(modeladmin, request, queryset):
    res= queryset.update(is_active= True)
    message= f'تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request, message)
    
def export_json(modeladmin, request, queryset):
    response= HttpResponse(content_type= 'application/json')
    serializers.serialize("json", queryset, stream= response)
    return response
#------------------زیرگروه های گروه کالاها -------------------------------------------------------------
class ProductGroupInstancelineAdmin(admin.TabularInline):
    model= ProductGroup
    extra=1

#-------------------------------------------------------------------------------
class GroupFilter(SimpleListFilter):
    title= 'گروه محصولات'
    parameter_name= 'group'
    
    def lookups(self, request, model_admin):
        sub_groups= ProductGroup.objects.filter(~Q(group_parent=None))
        groups= set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title,) for item in groups]
    
    def queryset(self, request, queryset):
        if self.value()!= None:
            return queryset.filter(Q(group_parent= self.value()))
        return queryset
            

#-------------------------------------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display= ('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group','count_produc_of_group')
    list_filter= (GroupFilter, 'is_active',)
    search_fields= ('group_title',)
    ordering= ('group_parent','group_title',)
    inlines= [ProductGroupInstancelineAdmin]
    actions= [de_active_product_group, active_product_group, export_json, ]    
    list_editable= ['is_active',]
    
    
    def get_queryset(self, *args, **kwargs):
        qs= super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)   
        qs= qs.annotate(sub_group= Count('groups'))    
        qs= qs.annotate(produc_of_group= Count('product_of_groups'))    
        return qs
    
    
    @short_description('تعداد زیرگروه ها' )
    @order_field('sub_group')
    def count_sub_group(self, obj):
        return obj.sub_group
    
    @short_description('تعداد کالاهای گروه')
    @order_field('produc_of_group')
    def count_produc_of_group(self, obj):
        return obj.produc_of_group
    
    count_sub_group.short_description= "تعداد زیرگروه ها"
    de_active_product_group.short_description= "غیر فعال کردن گروه های انتخاب شده"        
    active_product_group.short_description= " فعال کردن گروه های انتخاب شده"        
    export_json.short_description= "خروجی json  از گزوه های انتخاب شده"

#----------------ویژگی های کالا--------------------------------------------------------------------
class FeatureValueInstanceInline(admin.TabularInline):
    model= FeatureValue
    extra=3
    
#----------------ویژگی های کالا--------------------------------------------------------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display= ('feature_name','display_groups', 'display_feature_values')
    list_filter= ('feature_name',)
    search_fields= ('feature_name',)
    ordering= ('feature_name',)
    inlines=[FeatureValueInstanceInline, ]    
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs["queryset"]= ProductGroup.objects.filter(~Q(group_parent= None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def display_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    
    def display_feature_values(self, obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    
    display_groups.short_description= "گروه های دارای این ویژگی "        
    display_feature_values.short_description= "مقادیر ممکن برای این ویژگی "        
        
#-----------------فعال و غیر فعال کردن کالا-------------------------------------------------------------------
def de_active_product(modeladmin, request, queryset):
    res= queryset.update(is_active= False)
    message= f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

def active_product(modeladmin, request, queryset):
    res= queryset.update(is_active= True)
    message= f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)
    
#-------------------زیرگروه کالاها---------------------------------------------
class ProductFeatureInstanceInlineAdmin(admin.TabularInline):
    model= ProductFeature
    extra=5
    
    class Media:
        css= {
            'all': ('assets/css/admin_style.css', )
        }

        js= (
            'assets/js/ajax.js',
            'assets/js/admin_script.js', 
        )
#-------------------زیرگروه گالری تصاویر---------------------------------------------
class ProductProductGaleryInstanceInlineAdmin(admin.TabularInline):
    model= ProductGallery
    extra=3

#------------------------کالاها----------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  
    list_display= ('product_name', 'display_product_group','price','brand','is_active','update_date','slug',)
    list_filter= ('brand','product_group')
    search_fields= ('product_name',)
    ordering= ('update_date','product_name',)
    actions=[de_active_product, active_product,]
    inlines= [ProductFeatureInstanceInlineAdmin, ProductProductGaleryInstanceInlineAdmin, ]
    
    def display_product_group(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
       
    de_active_product.short_description= "غیر فعال کردن کالاهای انتخاب شده"        
    active_product.short_description= " فعال کردن کالاهای انتخاب شده"        
    display_product_group.short_description= "گروه های کالا"        
   
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name== 'product_group':
            kwargs["queryset"]= ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

#--------------------------چیدمان فرم ادمین----------------------------------------------------------
    fieldsets = (
        ("اطلاعات محصول", {"fields": (
            'product_name', 'price',
            'image_name',
            ('product_group', 'is_active', 'brand',),
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
