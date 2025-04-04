from django.views import View
from django.db.models import Q
from apps.products.models import Product 
from django.shortcuts import render, redirect



#اگر قراره یک صفحه کامل استفاده شود بهتره از کلاس استفادع شود
#__icontains یعنی نیاز نیست حتما اون کلمه ی خاص باشه حتی اگه توی کلمه وجود داشت هم بیار

class SearchResultsViews(View):
    def get(self, request, *args, **kwargs):    
        query= self.request.GET.get('q')     # برو از ادرس کیو را بیار
        
        products= Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )
        context={
            "products": products
        }
        return render(request, "search_app/search_results.html", context)
        