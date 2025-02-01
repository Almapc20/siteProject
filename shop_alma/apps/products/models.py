from django.db import models
from django.urls import reverse
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# -------------------------------------------------------------------------------------
class Brand(models.Model):
    brand_title= models.CharField(max_length=100, verbose_name='نام برند')
    file_upload= FileUpload('image', 'brand')
    image_name= models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر برند')
    slug= models.SlugField(max_length=200, null=True)
    
    def __str__(self):
        return self.brand_title
    
    class Meta:
        verbose_name= 'برند'
        verbose_name_plural= 'برند ها'

# #---------------------------------------------------------------------------------
class ProductGroup(models.Model):
    group_title= models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    file_upload= FileUpload('image', 'product_group')
    image_name= models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کروه کالا')
    # description= RichTextField(blank= True, null= True, verbose_name='توضیحات گروه کالا')
    description= RichTextUploadingField(config_name= 'special', blank= True)    
    is_active= models.BooleanField(default= True, blank= True, verbose_name='وضعیت فعال / غیر فعال')
    register_date= models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date=models.DateTimeField(default= timezone.now, verbose_name='تاریخ انتشار')
    update_date= models.DateTimeField(auto_now= True, verbose_name='تاریخ به روز رسانی')
    group_parent= models.ForeignKey('ProductGroup', on_delete=models.CASCADE, verbose_name='والد گروه کالا', blank= True, null= True, related_name= 'groups')
    slug= models.SlugField(max_length=200, null=True)
    
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name= 'گروه ها'
        verbose_name_plural= 'گروه های کالا'
    
# #---------------------------------------------------------------------------------
class Feature(models.Model):
    feature_name= models.CharField(max_length=100, verbose_name='عنوان ویژگی')
    product_group= models.ManyToManyField(ProductGroup, verbose_name='گروه غذاها', related_name='features_of_groups')
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name= 'ویژگی'
        verbose_name_plural= 'ویژگی ها'
    
    
# #---------------------------------------------------------------------------------
class Product(models.Model):
    product_name= models.CharField(max_length=500, verbose_name='نام کالا')
    summery_description= models.TextField(default="", blank= True, null= True, verbose_name= ' مختصری از توضیحات کالا')
    description= RichTextUploadingField(config_name= 'special', blank= True)    
    file_upload= FileUpload('image', 'product')
    image_name= models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price= models.PositiveIntegerField(default=0, verbose_name='قیمت کالا')
    is_active= models.BooleanField(default= True, blank= True, verbose_name='وضعیت فعال / غیر فعال')
    register_date= models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date=models.DateTimeField(default= timezone.now, verbose_name='تاریخ انتشار')
    update_date= models.DateTimeField(auto_now= True, verbose_name='تاریخ به روز رسانی')
    product_group= models.ManyToManyField(ProductGroup, verbose_name= 'گروه کالاها', related_name= 'products_of_groups')
    brand= models.ForeignKey(Brand, verbose_name='برند کالا', on_delete=models.CASCADE, null= True, related_name='brands')
    slug= models.SlugField(max_length=200, null=True)
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"slug": self.slug})
    
    
    class Meta:
        verbose_name= 'کالا'
        verbose_name_plural= 'کالا ها'
    
# #---------------------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100,verbose_name='عنوان مقدار')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,blank=True,null=True,verbose_name='ویژگی',related_name='feature_values')
    
    def __str__(self):
        return f"{self.id} {self.value_title}"
    
    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقدار ویژگی ها'
            

#------------------------------------------------------------------------------------------------------------------------------
class ProductFeature(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name= 'کالا', related_name='product_features')
    feature= models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name= 'ویژگی')
    value= models.CharField(max_length=100, verbose_name= 'مقدار ویژگی کالا')
    filter_value = models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار ویژگی برای فیلتر')        
    def __str__(self):
        return f"{self.product} - {self.feature} : {self.value}"
    
    class Meta:
        verbose_name= 'ویژگی کالا'
        verbose_name_plural= 'ویژگی های کالا'
    
# #---------------------------------------------------------------------------------
class ProductGallery(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name= 'کالا', related_name="gallery_images")
    file_upload= FileUpload('image', 'product_gallery')
    image_name= models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    
    class Meta:
        verbose_name= 'تصویر'
        verbose_name_plural= 'تصاویر'
    
# #---------------------------------------------------------------------------------
    