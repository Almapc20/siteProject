from django.urls import path,include
from .import views

app_name='payments'
urlpatterns = [
    # path('zarinpal_payment/<int:order_id>/',views.ZarinpalPaymentView.as_view(),name='zarinpal_payment'),
    # path('verify/<int:order_id>/',views.ZarinpalPaymentView.as_view(),name='zarinpal_payment_verify'),
    # path('show_verify_message/<str:message>/',views.show_verify_message,name='show_verify_message'),
    path('spot_payment/<int:order_id>',views.SpotPaymentVerifyView.as_view(),name='spot_payment'),
]