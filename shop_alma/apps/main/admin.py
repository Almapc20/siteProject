from django.contrib import admin
from .models import Slider
# --------------------------------------------------------------------------------------------------------

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_slide', 'slider_title1', 'link', 'is_active', 'register_date',)
    list_filter = ('slider_title1',)  # اضافه کردن فیلترهای بیشتر
    search_fields = ('slider_title1',)  # افزودن فیلدهای جستجو بیشتر
    ordering = ('update_date',)  # تغییر به ترتیب نزولی بر اساس تاریخ آخرین به روز رسانی
    readonly_fields = ('image_slide',)  # اگر فیلدهای دیگری نیاز به حالت خواندنی دارند، به اینجا اضافه کنید
