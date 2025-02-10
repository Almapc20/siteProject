from django.shortcuts import render, get_object_or_404
from .models import Product, ProductGroup, FeatureValue, Brand
from django.db.models import Q, Count, Min, Max
from django.views import View
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator


def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent= None))

#==========================ارزانترین محصولات=========================================
def get_cheapest_products(request, *args, **kwargs):
    products= Product.objects.filter(is_active= True).order_by('price')[:4]
    product_groups= get_root_group()
    context= {
        "products": products,
        "product_groups": product_groups
    }
    return render(request, "products_app/partials/cheapest_products.html", context)


#========================جدیدترین محصولات=======================================
def get_last_products(request, *args, **kwargs):
    products= Product.objects.filter(is_active= True).order_by('-published_date')[:4]
    product_groups= get_root_group()
    context= {
        "products": products,
        "product_groups": product_groups
    }
    return render(request, "products_app/partials/last_products.html", context)

#========================دسته های محبوب =======================================
def get_popular_product_group(request, *args, **kwargs):
    # product_groups= ProductGroup.objects.filter(Q(is_active=True)).annotate(count= Count('product_of_groups')).order_by('-count')[:6]
    product_groups= ProductGroup.objects.filter(Q(is_active=True))\
                    .annotate(count= Count('product_of_groups'))\
                    .order_by('-count')[:6]
                    
    context= {
        "product_groups": product_groups
    }
    return render(request, "products_app/partials/popular_product_group.html", context)

#========================جزئیات محصول =======================================
class ProductDetailView(View):
    def get(self, request, slug):
        product= get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, "products_app/product_detail.html", {'product':product})

#======================== محصولات مرتبط=======================================
def get_related_products(request, *args, **kwargs):
    curent_products= get_object_or_404(Product, slug=kwargs['slug'])
    related_products= []
    for group in curent_products.product_group.all() :
        related_products.extend(Product.objects.filter(Q(is_active=True) & (Q(product_group=group)) & ~Q(id= curent_products.id)))

    return render(request, "products_app/partials/related_product.html", {'related_products':related_products})

#======================== همه دسته ها =======================================
class ProductGroupView(View):   
    def get(self, request):
        product_groups= ProductGroup.objects.filter(Q(is_active=True))\
                        .annotate(count= Count('product_of_groups'))\
                        .order_by('-count')
        return render(request, "products_app/product_groups.html/", {'product_groups':product_groups})

#======================== لیت محصولات دسته ها =======================================
class ProductsByGroupView(View):
    def get(self,request, *args, **kwargs):        
        slug= kwargs['slug']
        current_group= get_object_or_404(ProductGroup, slug=kwargs['slug'])
        products= Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))     
        res_aggre= products.aggregate(min=Min('price'), max=Max('price'),)
            
        #price filter
        filter= ProductFilter(request.GET,queryset=products)
        products= filter.qs
        
        #brand filter
        brand_filter= request.GET.getlist('brand')
        if brand_filter:
            products=products.filter(brand__id__in=brand_filter)
            
        #features filter
        feature_filter= request.GET.getlist('feature')
        if feature_filter:
            products=products.filter(product_feature__filter_value__id__in= feature_filter).distinct()
            
        sort_type= request.GET.get('sort_type')
        if not sort_type:
            sort_type="0"
        
        if sort_type=="1":
            products= products.order_by('price')
        
        elif sort_type=="2":
            products= products.order_by('-price')
        
        group_slug= slug
        product_per_page=10                                     # تعداد کالاها در هر صفحه  
        paginator= Paginator(products, product_per_page)        #
        page_number= request.GET.get('page')                    # بدست آوردن شماره صفحه جاری
        page_obj= paginator.get_page(page_number)               # لیست کالاها بعد از صفحه بندی برای نمایش در صفحه جاری
        product_count= products.count()                         # تعداد کل کالاهای موجود در این گروه 
        
        # لیست اعداد برای ساخت منو باز شونده برای تعیین تعداد کالای هر صفحه توسط کاربر
        show_count_product= []
        i= product_per_page
        while i<product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)
        
        context={
            'products':products,
            'current_group': current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_count_product': show_count_product,
            'filter': filter,
            'sort_type': sort_type,
        }    
        
        return render(request, "products_app/products.html/", context)


#======================== جی کوئری ارتباط ویژگی ها =======================================
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id= request.GET["feature_id"]
        feature_values= FeatureValue.objects.filter(feature_id= feature_id)
        res= {fv.value_title:fv.id for fv in feature_values}

        return JsonResponse(data=res, safe=False)

#========================= لیست گروه محصولات برای فیلتر =======================================
def get_product_groups(request):
    product_groups= ProductGroup.objects.annotate(count= Count('product_of_groups'))\
                    .filter(Q(is_active= True) & ~Q(count=0))\
                    .order_by('-count')
    return render(request, 'products_app/partials/product_groups.html', {'product_groups': product_groups})

#========================= لیست برند ها برای فیلتر =======================================
def get_brands(request, *args, **kwargs):
    product_group= get_object_or_404(ProductGroup, slug= kwargs['slug'])
    brand_list_id= product_group.product_of_groups.filter(is_active=True).values('brand_id')
    brands= Brand.objects.filter(pk__in= brand_list_id)\
                        .annotate(count= Count('brands'))\
                        .filter(~Q(count=0))\
                        .order_by('-count')
    return render(request, 'products_app/partials/brands.html', {'brands': brands})

#========================= لیست های دیگر فیلترها بر حسب مقادیر ویژگیهای کالاهای درون گروه =======================================
def get_feautres_for_filter(request, *args, **kwargs):
    product_group= get_object_or_404(ProductGroup, slug= kwargs['slug'])
    feature_list= product_group.feature_of_groups.all()
    feature_dict= dict()
    for feature in feature_list:
        feature_dict[feature]= feature.feature_value.all()
    
    return render(request, 'products_app/partials/features_filter.html', {'feature_dict':feature_dict})




















