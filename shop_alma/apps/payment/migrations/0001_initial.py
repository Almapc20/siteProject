# Generated by Django 5.1.7 on 2025-03-14 12:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_customer_image_name'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ پرداخت')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش پرداخت')),
                ('amount', models.IntegerField(verbose_name='مبلغ پرداخت')),
                ('description', models.TextField(verbose_name='توضیخات پرداخت')),
                ('is_finally', models.BooleanField(default=False, verbose_name='وضعیت پرداخت')),
                ('status_code', models.IntegerField(blank=True, null=True, verbose_name='کد وضعیت درگاه پرداخت')),
                ('ref_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره پیگیری پرداخت')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_customer', to='accounts.customer', verbose_name='مشتری')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order', to='orders.order', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت ها',
            },
        ),
    ]
