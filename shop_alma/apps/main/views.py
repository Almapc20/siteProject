from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import Slider
from django.db.models import Q

def media_admin(request):
    return {'media_url':settings.MEDIA_URL,}

def index(request):
    return render(request, "main_app/index.html")


class sliderView(View):
    def get(self,request):
        sliders=Slider.objects.filter(Q(is_active=True))
        return render(request,"mainapp/sliders.html",{"sliders":sliders})


def handler404(request,exception=None):
    return render(request,'mainapp/404.html')