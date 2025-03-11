from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from .models import Order,OrderDetail,PaymentType
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
import utils
#============================================================================
class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request,'orders_app/shop_cart.html', {'shop_cart': shop_cart})
    
#----------------------------------------------------------------------------------------
def show_shop_cart(request):
    shop_cart=ShopCart(request)
    total_price= shop_cart.calc_total_price()
    delivery= 25000
    if total_price> 500000:
        delivery= 0

    tax= int(0.09* total_price)
    order_final_price= int(total_price+ delivery+ tax)
    context={
        'shop_cart': shop_cart,
        'total_price': total_price,
        'delivery': delivery,
        'tax': tax,
        'order_final_price': order_final_price,
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
    shop_cart.update(product_id_list, qty_list)
    return redirect("orders:show_shop_cart")

#-----------------------------------------------------------------------------------
def status_of_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)
# ===============================================================================
class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request):
        
        try:
            customer=Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer=Customer.objects.create(user=request.user)
            
        order=Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType,id=1))
        shop_cart=ShopCart(request)
        for item in shop_cart:
            OrderDetail.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                qty=item['qty']
            )
        return redirect('orders:checkout_order',order.id)
    
# ===============================================================================================
class CheakoutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        user=request.user
        customer=get_object_or_404(Customer,user=user)
        shop_cart=ShopCart(request)
        order=get_object_or_404(Order,id=order_id) 
        
        total_price=shop_cart.calc_total_price()
        delivery=25000
        if total_price>500000:
            delivery=0
        tax=0.09*total_price
        order_final_price=total_price+delivery+tax
        
        if (order.discount or 0) > 0:
            order_final_price = order_final_price - (order_final_price * order.discount / 100)
        
        # order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
        
        
        data={
            'name':user.name,
            'family':user.family,
            'email':user.email,
            'phone_number':customer.phone_number,
            'address':customer.address,
            'description':order.description,
            'payment_type':order.payment_type
        }
        
        form=OrderForm(data)
        
        form_coupon = CouponForm() 

        context={
            'shop_cart':shop_cart,
            'total_price':total_price,
            'delivery':delivery,
            'tax':tax,
            'order_final_price':order_final_price,
            'order':order,
            'form':form,
            'form_coupon' : form_coupon
        }
        return render(request,'orders_app/checkout.html',context)
#-----------------------------------------------------------------------
# class ApplyCoupon(View):
#     def post(self, request, *args, **kwargs):
#         order_id = kwargs['order_id']
#         coupon_form = CouponForm(request.POST)
#         if coupon_form.is_valid():
#             cd = coupon_form.cleaned_data
#             coupon_code = cd['coupon_code']


#         # شرایط تایید کوپن
#             coupon = Coupon.objects.filter(
#                 Q(coupon_code=coupon_code) &
#                 Q(is_active=True) &
#                 Q(start_date__lte=datetime.now()) &
#                 Q(end_date__gte=datetime.now())
#             )
#             discount=0
            
#             try:
#                 order = Order.objects.get(id=order_id)
#                 if coupon.exists():
#                     discount = coupon[0].discount
#                     order.discount = discount
#                     order.save()
#                     messages.success(request, "اعمال کوپن با موفقیت انجام شد")
#                     return redirect('orders:checkout_order', order_id)
#                     # return redirect('payments:zarinpal_payment', order_id) # این کد رو وقتی کدای زرین پال نوشتیم اجراش می کنیم
#                 else:
#                     order.discount=discount
#                     order.save()
#                     messages.error(request, "کد وارد شده معتبر نمی‌باشد", 'danger')
#             except ObjectDoesNotExist:
#                 messages.error(request, "سفارش موجود نیست")
        
class ApplyCoupon(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        coupon_form = CouponForm(request.POST)

        if coupon_form.is_valid():
            cd = coupon_form.cleaned_data
            coupon_code = cd.get('coupon_code', None)  # ✅ جلوگیری از KeyError

            if not coupon_code:
                messages.error(request, "کد کوپن ارسال نشده است", 'danger')
                return redirect('orders:checkout_order', order_id)
        else:
            messages.error(request, "فرم نامعتبر است. لطفاً دوباره تلاش کنید.", 'danger')
            return redirect('orders:checkout_order', order_id)

        coupon = Coupon.objects.filter(
            Q(coupon_code=coupon_code) &
            Q(is_active=True) &
            Q(start_date__lte=datetime.now()) &
            Q(end_date__gte=datetime.now())
        )

        discount = 0
        try:
            order = Order.objects.get(id=order_id)
            if coupon.exists():
                discount = coupon.first().discount  # ✅ استفاده از `.first()` به‌جای `[0]`
                order.discount = discount
                order.save()
                messages.success(request, "اعمال کوپن با موفقیت انجام شد")
            else:
                messages.error(request, "کد وارد شده معتبر نمی‌باشد", 'danger')

            return redirect('orders:checkout_order', order_id)

        except ObjectDoesNotExist:
            messages.error(request, "سفارش موجود نیست")
            return redirect('orders:checkout_order', order_id)
