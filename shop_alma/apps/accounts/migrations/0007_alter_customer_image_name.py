# Generated by Django 5.1.7 on 2025-03-24 09:56

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customer_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر پروفایل'),
        ),
    ]
