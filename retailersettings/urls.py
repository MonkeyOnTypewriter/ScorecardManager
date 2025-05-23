from django.urls import path
from . import views

urlpatterns = [
    path('product_form/<str:brandingcode_id>/', views.product_form, name='product_form'),
    path('loan_forms/', views.get_loan_forms, name='loan_forms'),
    path('filter_creditlines/', views.filter_creditlines, name='filter_creditlines'),
    path('filter_promos/', views.filter_promos, name='filter_promos'),
    path('filter_fees/', views.filter_fees, name='filter_fees'),
    path('product_creation_success/', views.product_creation_success, name='product_creation_success'),
    path('retailer_options/', views.retailer_options, name='retailer_options'),
    path('filter_brandingcodes/', views.filter_brandingcodes, name='filter_brandingcodes'),
    path('product_detail/<str:product_id>/', views.product_detail, name='product_detail'),
    path('product_list/<str:brandingcode_id>/', views.list_brandingcode_products, name='list_brandingcode_products'),
    path('product_detail_options/<str:product_id>/', views.product_detail_options, name='product_detail_options'),
]