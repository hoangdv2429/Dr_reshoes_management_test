from home.forms import search_cus_data_phone_num
from home.models import Cashier
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('contact/', views.contact),
    path('login/',views.login),
    path('home/all_worker_infos/',views.all_worker_infos),
    path('home/all_cashier_infos/', views.all_cashier_infos),
    path('home/cal_salary_worker/', views.cal_salary_worker),
    path('home/cal_salary_cashier/', views.cal_salary_cashier),
    path('cashier/',views.Cashier),
    path('login/home/show_untouch_shoes/',views.show_untouch_shoes),
    path('login/home/show_done_not_yet_return/',views.show_done_not_yet_return),
    path('login/home/re_in/', views.receipt),
    path('login/home/search_cus_data_phone_num/',views.search_cus_data_phone_num),
    path('login/home/se_in', views.service_in)
]
#chay di 
