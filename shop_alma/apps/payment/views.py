# from django.shortcuts import render,redirect
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import ObjectDoesNotExist
# from apps.orders.models import Order
# from .models import Payment
# from apps.accounts.models import Customer
# import requests
# import json
# from django.http import HttpResponse 

from django.shortcuts import render,redirect
from django .views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order,OrderState
import requests
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment
from apps.accounts.models import Customer
from apps.warehouses.models import Warehouse, WarehousesType
from django.http import HttpResponse 

#-------------------------------------------------------------
# MERCHANT='XXXXX-XXX-XXXX-XXX-XXX-XXX-XXX-XXX'
# ZP_API_REQUEST = f"https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = f"https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/{{authority}}"

# CallbackURL = 'http://127.0.0.1:8000/payments/verify/' 
# #------------------------------------------------------------
# class ZarinpalPaymentView(LoginRequiredMixin,View):
#         def get(self,request,order_id):
#         try:
#                 description='پرداخت از طریق درگاه زرین پال انجام می شود'
#                 order=Order.objects.get(id=order_id)
#                 payment=Payment.object.create(
#                     description="پرداخت از طریق درگاه زرین پال انجام میشود."
#                     order=order,
#                     customer=Customer.objects.get(user=request.user),
#                     amount=order.get_order_total_price(),
#                     "description": description,
#                 )
#                 payment.save()
              
#                 request.session['payment_session']={
#                   'order_id':order.id,
#                   'payment_id':payment.id
#                 }
#                 user=request.user 
#                 req_data = {
#                 "MerchantID": MERCHANT,
#                 "amount": order.get_order_total_price(),
#                 "description": description,
#                 "CallbackURL": CallbackURL,
#                 "metadate":{"mobile":user.mobile_number,"email":user.email}
#                 }
#                 req_header={"accept":"application/json","content_type":"application/json"}
#                 req=request.post(url=ZP_API_REQUEST,data=json.dumps(req_data),headers=req_header)
#                 authority=req.json()['data']['authority']
#                 if len(req.json()['errors'])==0:
#                     return redirect(ZP_API_STARTPAY.format(authority=authority))
#                 else:
#                     e_code=req.json()['errors']['code']
#                     e_message=req.json()['errors']['message']
#                     return HttpResponse(f"ERROR code:{e_code}, Error Message:{e_message}")
#         except ObjectDoesNotExist:
#             raise redirect('orders:checkout_order',order_id)
        
#-------------------------------------------------------------------------------------------
# class ZarinpalPaymentVeryfyView(LoginRequiredMixin, View):
#     def get(self,request):
#         
#         t_status = request.GET.get('Status')
#         t_authority = request.GET.get('Authority')
#         if request.GET.get('Status') == 'OK' :
#             order_id=request.session['payment_session']['order_id']
#             payment_id=request.session['payment_session']['payment_id']
#             order=Order.objects.get(id=order_id)
#             payment=Payment.objects.get(id=payment_id)
            
#             req_header = {'accept': 'application/json','content-type':'application/json'}
#             req_data = {
#                 "merchant_id": MERCHANT,
#                 "amount":order.get_order_total_price(),
#                 't_authority':t_authority
#             }
#             req=request.post(url=ZP_API_VERIFY,data=json.dumps(req_data),headers=req_header)
#             if len(req.json()['errors']) == 0 : 
#                 t_status = req.json()['data']['code']
#                 if t_status == 100:
#                     order.is_finally=True
#                     order.order_state=OrderState.objects.get(id=1)
#                     order.save()
                    
                
#                     payment.is_finally=True
#                     payment.status_code=t_status
#                     payment.ref_id=str(req.json()['data']['ref_id'])
#                     payment.save()
#

#                     return redirect("payments:show_verify_message ",f"پرداخت با موفقیت انجام شد, کد رهگیری شما{str(req.json()['data']['ref_id'])}")
                
#                 elif t_status == 101:
#                     order.is_finally=True
#                     order.order_state=OrderState.objects.get(id=1)
#                     order.save()           
                    
#                     payment.is_finally=True
#                     payment.status_code=t_status
#                     payment.ref_id=str(req.json()['data']['ref_id'])
#                     payment.save()
                      
                    
#                     return redirect("payments:show_verify_message ",f"پرداخت قبلا انجام شد, کد رهگیری شما{str(req.json()['data']['ref_id'])}")
               
               
#                 else:
#                     payment.status_code=t_status
#                     payment.save()
#                     return HttpResponse('payments:show_verify_message',f"خطا در فرایند چرداخت کد وضعیت : {t_status}")
                
#             else:
#                 e_code = req.json()['errors']['code']
#                 e_message = req.json()['errors']['message']
#                 return redirect("payments:show_verify_message",f" خطا در فرایند پرداخت کد خطا : Error : code : {e_code},Error Message: {e_message}")
            
#         else:
#             return redirect("payments:show_verify_message",f" خطا در فرایند پرداخت کد خطا ")
    
# #---------------------------------------------------------------------------------------
# def show_verify_message(request,message):
#     return render(request,"payments/verify_message.html",{'message':message})

#=================================================================================================
class SpotPaymentVerifyView(LoginRequiredMixin,View):
      def get(self, request, order_id):              
            description="پرداخت از طریق پرداخت در محل انجام می شود"
            try:           
                order=Order.objects.get(id= order_id)
                payment= Payment.objects.create(
                order= order,
                customer= Customer.objects.get(user= request.user),
                amount= order.get_order_total_price(),
                description= description,
                )
                payment.save()

                order=Order.objects.get(id= order_id)
                order.is_finaly= True
                order.order_state=OrderState.objects.get(id=1)
                order.save()
                payment.is_finaly= True
                payment.save()    
                  
                for item in order.orders_details1.all():
                    Warehouse.objects.create(
                        warehouse_type= WarehousesType.objects.get(id= 2),
                        user_registered= request.user,
                        product= item.product,
                        qty= item.qty,
                        price= item.price
                    )
                return redirect('main:index')

            except:
                return redirect('orders:checkout_order', order_id)