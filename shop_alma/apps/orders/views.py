from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse
import utils
#============================================================================

class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request,'orders_app/shop_cart.html', {'shop_cart': shop_cart})
    
#----------------------------------------------------------------------------------------
def show_shop_cart(request):
    shop_cart=ShopCart(request)
    total_price=shop_cart.calc_total_price()
    delivery=25000
    if total_price>500000:
        delivery=0
    tax=0.09*total_price
    order_final_price=total_price+delivery+tax
    
    # order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
    context={
        'shop_cart': shop_cart,
        'shop_cart_count':shop_cart.count,
        'total_price':total_price,
        'delivery':delivery,
        'tax':tax,
        'order_final_price':order_final_price
    }
    return render(request, 'orders_app/partials/show_shop_cart.html',context)

#---------------------------------------------------------------------------------------
def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty=request.GET.get('qty')
    
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,qty)
    return HttpResponse(shop_cart.count)
#----------------------------------------------
def delete_from_shop_cart(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")
    
#-------------------------------------------------------
def update_shop_cart(request):
    product_id_list=request.GET.getlist('product_id_list[]')
    qty_list=request.GET.getlist('qty_list[]')
    shop_cart=ShopCart(request)
    shop_cart.update(product_id_list,qty_list)
    return redirect("orders:show_shop_cart")

#-----------------------------------------------------------------------------------
def statuse_of_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)

