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
    products= Product.objects.filter(is_active=True).order_by('price')[:6]
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
