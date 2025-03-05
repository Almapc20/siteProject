from django.shortcuts import render
from django.views import View
from .shop_cart import ShopCart
#--------------------------------------------------------------------


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