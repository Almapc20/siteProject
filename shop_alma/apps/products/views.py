from django.shortcuts import render, get_object_or_404
from .models import Product, ProductGroup, Brand
from django.db.models import Q, Count, Min, Max
from django.views import View
from django.http import JsonResponse

from django.core.paginator import Paginator
#---------------------------------------------------------------------------------------------------------------
def root_group():
    return ProductGroup.objects.filter(Q(is_active=True)& Q(group_parent=None))

# -----------------------------ارزانترین محصولات که بر اساس قیمت مرتب شده اند----------------------------------
def get_cheapest_products(request, *args, **kwargs):
    products= Product.objects.filter(is_active=True).order_by('price')[:4]
    product_groups=root_group()
    context={
        'products' : products,
        'product_groups': product_groups,
    }
    return render(request, "products_app/partials/cheapest_products.html", context)

# -----------------------------جدیدترین محصولات به روز شده ----------------------------------
def get_last_products(request, *args, **kwargs):
    products= Product.objects.filter(is_active=True).order_by('-published_date')[:4]
    product_groups=root_group()
    context={
        'products' : products,
        'product_groups': product_groups,
    }
    return render(request, "products_app/partials/last_products.html", context)

#========================دسته های محبوب =======================================
def get_popular_product_groups(request,*args,**kwargs):
    product_groups=ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups')).order_by('-count')[:6]
    context={
        'product_groups':product_groups
    }
   
    return render(request, "products_app/partials/popular_product_group.html", context)

#========================جزئیات محصول =======================================
class ProductDetailView(View):
    def get(self, request, slug):
        product= get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, "products_app/product_detail.html", {'product':product})

# ======================محصولات مرتبط =========================================================
def get_related_products(request,*args,**kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,'products_app/partials/related_products.html',{'related_products':related_products})

# لیست همه گروه های محصولات ========================================================================================================
class ProductGroupView(View):
    def get(self,request):
        product_groups=ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups'))\
                                                                     .order_by('-count')
        
        return render(request,'products_app/product_groups.html/',{'product_groups':product_groups})
# لیست گروه محصولات برای فیلتر--------------------------------------------------------------------------------------------------------------------------------------------
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                                       .filter(Q(is_active=True) & ~Q(count=0))\
                                                       .order_by('-count')
    
    return render(request, 'products_app/partials/product_groups.html' ,{'product_groups':product_groups})

# لیست برندها برای فیلتر-# -----------------------------------------------------------------------------------------------------------------------------------------
def get_brands(request,*args,**kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id=product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brand=Brand.objects.filter(pk__in=brand_list_id)\
        .annotate(count=Count('brands'))\
        .filter(~Q(count=0))\
        .order_by('-count')
    
    return render(request,'products_app/partials/brands.html',{'brand':brand, 'group_slug': kwargs['slug']})
# #--لیست دیگر ویزگی ها بر حسب ویزگی های کالاهای درون گروه---------------------------------------------------------------------------------------------------------------

def get_features_for_filter(request,*args,**kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list=product_group.features_of_groups.all()
    feature_dict=dict()
    
    for feature in feature_list :
        feature_dict[feature]=feature.feature_values.all();
    
    return render(request,'products_app/partials/features_filter.html',{'feature_dict':feature_dict})
        
# #-لیست محصولات هر گروه محصولات--------------------------------------------------------------------------------------------------------------
class ProductByGroupView(View):
    def get(self,request,*args,**kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup,slug=slug)   #برو از پروداکت گروپ اسلاگ ها رو بیاور 
        products = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
       
        #اگر خواستی روی یه مجموعه ای یسری تابع اعمال کنی از aggregate استفاده میکنیم
        res_aggre=products.aggregate(min=Min('price'),max=Max('price'))
         
        
        #price filter
        filter=ProductFilter(request.GET,queryset=products)
        products=filter.qs 
        
        
        #queryset=      لیستی که قراره فیلتر روی اون اعمال بشه
        
        #brand filter
        brands_filter=request.GET.getlist('brand')
        if brands_filter:
            products=products.filter(brand__id__in=brands_filter )
               
            
        #feature filter
        features_filter=request.GET.getlist('feature')
        if features_filter:
            products=products.filter(product_feature__filter_value__id__in=features_filter ).distinct()
            
        #distinct       حذف تکراری ها 
            
    
            
        group_slug=slug 
        product_per_page=10                         #تعداد کالاها در هر صفحه
        paginator=Paginator(products, product_per_page)         
        page_number=request.GET.get('page')                   #بدست اوردن شماره صفحه جاری
        page_obj=paginator.get_page(page_number)              #لیست کالا ها بعد از صفحه بندی برای نمایش در صحفه جاری
        product_count=products.count();                       #تعداد کل کالاهای موجود در این گروه
        
        
        #لیست اعداد برای ساخت منو باز شونده برای تعیین تعداد کالای هر صففحه توسط کاربر
        show_count_product=[]
        i=product_per_page
        while i<product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)


        context={
            'products':products,
            'current_group':current_group,
            'res_aggre':res_aggre,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'show_count_product':show_count_product,
             'filter':filter,
            
        }            
    
        
 

        return render(request,"products_app/products.html",{"products":products,'current_group':current_group})

        
