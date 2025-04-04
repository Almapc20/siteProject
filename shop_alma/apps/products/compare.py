
#اگر نمونه ای ازین کلاس بسازیم میتونیم به یه لیست که از جنس سشنه بهش اضافه کنیم یا حذف کنیم
#لیستی که قراره در ان کد کالاها اضافه شود

class CompareProduct:
    def __init__(self,request):
        self.session = request.session 
        compare_product = self.session.get("compare_product")
        if not compare_product:
            compare_product=self.session["compare_product"]=[]  #بیا یه سشن خالی بساز و یه لیست خالی را بهش نسبت بده
        self.compare_product=compare_product
        self.count=len(compare_product)


#-----------------------------------------------------
    #ایتریبل کردن 
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item
            
#-----------------------------------------------------
    # اد کردن به لیست
    def add_to_compare_product(self,productId):
        productId =int(productId)
        if productId not in self.compare_product:
            self.compare_product.append(productId)
        self.count=len(self.compare_product)
        self.session.modified=True
        
#-----------------------------------------------------
    #حذف کردن از لیست
    def delete_from_compare_product(self,productId):
        self.compare_product.remove(int(productId))
        self.count=len(self.compare_product)
        self.session.modified=True
        
#-----------------------------------------------------
    #پاک کردن کل لیست
    def clean_compare_product(self):
        del self.session['compare_product']
        self.session.modified=True

