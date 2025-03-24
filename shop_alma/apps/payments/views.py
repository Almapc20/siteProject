from django.shortcuts import render,redirect
from django .views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
# import requests
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment
from apps.accounts.models import Customer
# from apps.warehouses.models import Warehouse, WarehousesType

#=================================================================================================
MERCHANT='xxxxxx-xxxxxxxx-xxxxxxxx-xxxxxx'
ZP_API_REQUEST = f"https://zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'


class ZarinpalPaymentView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        description="پرداخت از طریق درگاه زرین پال انجام شد"
        try:
            order=Order.objects.get(id=order_id)
            payment=Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=request.user),
                amount=order.get_order_total_price(),
                description=description,
            )
            payment.save()
            request.session['payment_session']={
                "order_id":order_id,
                "payment_id":payment.id
            }            
            user= request.user
            req_data = {
            "MerchantID": MERCHANT,
            "Amount": order.get_order_total_price(),
            "CallbackURL": CallbackURL,
            "Description":description ,
            "Phone": {"mobile": user.mobile_number, "mail": user.email },
            }   
            data = json.dumps(req_data)
            req_headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            try:
                response = requests.post(ZP_API_REQUEST, data=data,headers=req_headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                    
                return response
            
            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}
        
        except ObjectDoesNotExist:
            return redirect('orders:checkout_order',order_id) 
    # set content length by data

#=================================================================================================
class ZarinpalPaymentVerifyView(LoginRequiredMixin,View):
    def get(self, request):
            order_id=request.session['payment_session']['order_id']
            payment_id=request.session['payment_session']['payment_id']
            order=Order.objects.get(id=order_id)
            payment=Payment.objects.get(id=payment_id)
            authority=request.GET['Authority']
            
            data = {
                "MerchantID": MERCHANT,
                "Amount": order.get_order_total_price(),
                "Authority": authority,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    order.is_finaly=True
                    order.save()
                    
                    payment.is_finaly=True
                    payment.status_code=int(response['Status'])
                    payment.ref_id=str(response['RefID'])
                    payment.save()
            
                    # for orderdetail in order.orders_details1.all():
                    #     Warehouse.objects.create(
                    #         Warehouse_type=WarehousesType.objects.get(id=2),
                    #         user_registered=request.user,
                    #         product= orderdetail.product,
                    #         qty=orderdetail.qty,
                    #         price=orderdetail.price
                    #     )
                    
                    return {'status': True, 'RefID': response['RefID']}
                else:
                    payment.status_code=int(response['Status'])
                    payment.save()
                    return {'status': False, 'code': str(response['Status'])}
            return response

#=================================================================================================
class SpotPaymentVerifyView(LoginRequiredMixin,View):
      def get(self, request,order_id):              
            description="پرداخت از طریق پرداخت در محل انجام می شود"
            try:           
                order=Order.objects.get(id=order_id)
                payment=Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=request.user),
                amount=order.get_order_total_price(),
                description=description,
                )
                payment.save()

                order=Order.objects.get(id=order_id)
                order.is_finaly=True
                order.save()
                
                payment.is_finaly=True
                payment.save()    

                # for orderdetail in order.orders_details1.all():
                #     Warehouse.objects.create(
                #     # Warehouse_type=WarehousesType.objects.get(id=2),
                #     user_registered=request.user,
                #     product= orderdetail.product,
                #     qty=orderdetail.qty,
                #     price=orderdetail.price
                #     )
                return redirect('main:index')

            except:
                return redirect('orders:checkout_order',order_id)
