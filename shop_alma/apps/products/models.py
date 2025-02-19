from django.db import models
from email.mime import image
from utils import FileUpload
from django.utils import timezone
from django.urls import reverse
# from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from datetime import datetime

#------------------------------------------------------------------------------------------------------- 



class Brand(models.Model):
    brand_title= models.CharField(max_length=100, verbose_name="نام برند")
    file_uplaod= FileUpload('images', 'brand')
    slug= models.SlugField(max_length=200, null=True)
    image_name= models.ImageField(upload_to=file_uplaod.upload_to, verbose_name="تصویر گروه کالا")
    
    def __str__(self) -> str:
        return self.brand_title
    
    class Meta:
        verbose_name= "برند"
        verbose_name_plural= "برند ها"

#-----------------------------------------------------------------------------------
class ProductGroup(models.Model):
    group_title= models.CharField(max_length=100, verbose_name="عنوان گروه کالا")
    file_uplaod= FileUpload('images', 'product_group')
    image_name= models.ImageField(upload_to=file_uplaod.upload_to, verbose_name="تصویر گروه کالا")
    description= models.TextField(blank=True, verbose_name="توضیحات گروه کالا", null=True)
    is_active= models.BooleanField(default=True,blank=True, verbose_name="وضعیت فعال / غیر فعال")
    group_parent= models.ForeignKey('ProductGroup', on_delete=models.CASCADE, verbose_name="والد گروه کالا", blank=True, null=True, related_name='groups')
    slug= models.SlugField(max_length=200, null=True)
    register_date= models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج", )
    published_date= models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    update_date= models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین بروزرسانی")
    
    
    def __str__(self) -> str:
        return self.group_title
    
    class Meta:
        verbose_name= "گروه کالا"
        verbose_name_plural= "گروه های کالا"
    
#-----------------------------------------------------------------------------------
class Feature(models.Model):
    feature_name= models.CharField(max_length=100, verbose_name="نام ویژگی")    
    product_group= models.ManyToManyField(ProductGroup, verbose_name="گروه کالا",related_name="feature_of_groups")
    
    def __str__(self) -> str:
        return self.feature_name
    
    class Meta:
        verbose_name= "ویژگی کالا"
        verbose_name_plural= "ویژگی های کالا"
    
#-----------------------------------------------------------------------------------
class Product(models.Model):
    product_name= models.CharField(max_length=500, verbose_name="نام کالا")
    summery_description= models.TextField(default="", blank=True, null=True, verbose_name="توضیحات کالا")    
    description= RichTextUploadingField(config_name= 'special', blank= True)    
    # description=CKEditor5Field('Text', config_name='extends', blank= True)    
    file_uplaod= FileUpload('images', 'product')
    image_name= models.ImageField(upload_to=file_uplaod.upload_to, verbose_name="تصویر کالا")
    price= models.PositiveIntegerField(default=0, verbose_name="قیمت کالا")
    product_group= models.ManyToManyField(ProductGroup,verbose_name="گروه کالا", related_name="product_of_groups")
    features= models.ManyToManyField(Feature, through="ProductFeature")
    brand= models.ForeignKey(Brand, verbose_name="برنند کالا", on_delete=models.CASCADE, null=True, related_name="brands")
    is_active= models.BooleanField(default=True,blank=True, verbose_name="وضعیت فعال / غیر فعال")
    slug= models.SlugField(max_length=200, null=True)
    register_date= models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج", )
    published_date= models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    update_date= models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین بروزرسانی")
    
    def __str__(self) -> str:
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"slug": self.slug})
    
    
    #قیمت با تخفیف کالا
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active == True and 
                dbd.discount_basket.start_date <= datetime.now() and 
                datetime.now() <= dbd.discount_basket.end_date):
                list1.append(dbd.discount_basket.discount)
        discount=0
        if(len(list1)>0):
            discount=max(list1)
    
        return self.price-(self.price*discount/100)
    
    class Meta:
        verbose_name= " کالا"
        verbose_name_plural= "کالا ها"
    
#-----------------------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title= models.CharField(max_length=100, verbose_name="عنوان مقدار")
    feature= models.ForeignKey(Feature, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ویژگی", related_name="feature_value")
    
    def __str__(self) -> str:
        return f"{self.value_title}"
    
    class Meta:
        verbose_name= " مقدار ویژگی"
        verbose_name_plural= "مقادیر ویژگی ها"
    
#-----------------------------------------------------------------------------------
class ProductFeature(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE, verbose_name="کالا", related_name='product_features')
    feature= models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="ویژگی")
    value= models.CharField(max_length=100, verbose_name="مقدار ویژگی کالا")
    
    filter_value=  models.ForeignKey(FeatureValue, null=True, blank=True, on_delete= models.CASCADE, verbose_name="product_feature_value")
    
    def __str__(self):
        return f"{self.product} - {self.feature} - {self.value}"
    
    class Meta:
        verbose_name= "ویژگی کالا"
        verbose_name_plural= "ویژگی ها ی کالا ها"
    
#-----------------------------------------------------------------------------------
class ProductGallery(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا", related_name='galery_images')
    file_uplaod= FileUpload('images', 'product_gallery')
    image_name= models.ImageField(upload_to=file_uplaod.upload_to, verbose_name="تصویر کالا")
    
    
    class Meta:
        verbose_name= "تصویر"
        verbose_name_plural= "تصویر ها"
    
#-----------------------------------------------------------------------------------
    
    
    
    
    
    