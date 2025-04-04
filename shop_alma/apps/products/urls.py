from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('cheapest_products/', views.get_cheapest_products, name="cheapest_products"),
    path('last_products/', views.get_last_products, name="last_products"),
    path('popular_product_group/', views.get_popular_product_group, name="popular_product_group"),
    path('product_details/<slug:slug>/', views.ProductDetailView.as_view(), name="product_details"),
    path('related_product/<slug:slug>/', views.get_related_products, name="related_product"),
    path('product_groups/', views.ProductGroupView.as_view(), name="product_groups"),
    path('products_of_group/<slug:slug>/', views.ProductsByGroupView.as_view(), name="products_of_group"),
    path('ajax_admin/', views.get_filter_value_for_feature, name="filter_value_for_feature"),
    path('product_groups_partial/', views.get_product_groups, name="product_groups_partial"),
    path('brands_partial<slug:slug>/', views.get_brands, name="brands_partial"),
    path('features_for_filter<slug:slug>/', views.get_feautres_for_filter, name="features_for_filter"),
    path('shop/', views.ProductAllView.as_view(), name="shop"),
    path("status_of_compare_list/", views.status_of_compare_list, name="status_of_compare_list"),
    path("compare_table/",views.compare_table,name="compare_table"),
    path("add_to_compare_list/", views.add_to_compare_list, name="add_to_compare_list"),
    path("delete_from_compare_list/", views.delete_from_compare_list, name="delete_from_compare_list"),

]













