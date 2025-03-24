from django.urls import path
from .import views

app_name='payments'
urlpatterns = [
    path('zarinpal_payment/<int:order_id>',views.ZarinpalPaymentView.as_view(),name='zarinpal_payment'),
    path('spot_payment/<int:order_id>',views.SpotPaymentVerifyView.as_view(),name='spot_payment'),
    
]























