from home.models import Worker
from django.shortcuts import render
from django.http import HttpResponse
from .forms import loginForm, receipt_in, search_cus_data_phone_num, service_in
from django.template import loader
import psycopg2
from collections import namedtuple

from .models import Cashier, Worker, Customer
conn = psycopg2.connect(database = 'shoes_spa',user = 'postgres',password ='admin',host='localhost',port='5432') #ket noi vao database = conn
cur = conn.cursor()
# Create your views here.

def index(request):
    return render(request, 'pages/home.html')

def home(request):
    return render(request, 'pages/home.html')

# bắt đầu từ đây

def get_current_date(request):
    cur.execute("select current_date")
    data = cur.fetchall()
    print(data)
    context ={
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def all_worker_infos(request): 

    cur.execute("select * from worker")
    # data = cur.fetchone()
    data = dictfetchall(cur)
    context={
        'data' :data
    }
    return render(request, 'pages/all_worker_infos.html', context)

def search_worker_info_phone_num(request, phone_num):
    cur.execute("select * from worker where worker.phone_num = '%s'" % phone_num)
    data = cur.fetchall()
    context={
        'data' : data
    }    
    return render(request, 'pages/home.html',context)

def search_worker_info_id(request, id):
    cur.execute("select * from worker where worker.worker_id = '%s'" % id)
    data = cur.fetchall()
    context={
        'data' : data
    }    
    return render(request, 'pages/home.html',context)

def all_cashier_infos(request):
    cur.execute("select * from cashier")
    data = dictfetchall(cur)
    context={
        'data' :data
    }
    return render(request, 'pages/all_cashier_infos.html', context)

def search_cashier_info_phone_num(request, phone_num):
    cur.execute("select * from cashier where worker.cashier = '%s'" % phone_num)
    data = cur.fetchall()
    context={
        'data' : data
    }    
    return render(request, 'pages/home.html',context)

def search_cashier_info_id(request, id):
    cur.execute("select * from cashier where cashier.cashier_id = '%s'" % id)
    data = cur.fetchall()
    context={
        'data' : data
    }    
    return render(request, 'pages/home.html',context)

def cal_salary_cashier(request):
    cur.execute("select c.cashier_id, c.name, (num_of_work_days * 120000) paycheck from cashier c")
    data = dictfetchall(cur)
    print(data)
    context = {
        'data' :data
    }
    return render(request, 'pages/cal_salary_cashier.html', context)

def cal_salary_worker(request):
    cur.execute("select w.worker_id, w.name, sum(s.price*0.22) paycheck from worker w, _services s where w.worker_id = s.worker_id group by  w.worker_id")
    data = dictfetchall(cur)
    print(data)
    context = {
        'data' : data
    }
    return render(request, 'pages/cal_salary_worker.html', context)

def cashier_also_worker(request):
    cur.execute("select w.* from worker w, cashier c where w.phone_num = c.phone_num")
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def all_customer_infos(request):
    cur.execute("select * from customer")
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def show_past_receipt_phone_num(request, phone_num):
    cur.execute("select r.* from customer c, receipt r where c.customer_id = r.customer_id and c.phone_number = '%s'" % phone_num)
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def show_services_status_receipt_id(request, receipt_id):
    cur.execute("select * from _services s, receipt r where r.receipt_id = s.receipt_id and  r.receipt_id = '%s'" % receipt_id)
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def show_all_payment_of_customer(request, customer_id):
    return

def receipt_taken_by(request, receipt_id):
    cur.execute("select r.cashier_id from receipt r where r.receipt_id = '%s'" % receipt_id)
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def services_worker(request, receipt_id):
    cur.execute("select s.service_id, s.worker_id from receipt r, _services s where r.receipt_id = s.receipt_id and r.receipt_id = '%s'" % receipt_id)
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

def show_done_not_yet_return(request):
    cur.execute("select r.taken_day, r.receipt_id, s.service_id from receipt r, _services s where r.receipt_id = s.receipt_id and s.status = 'done' and s.return_day is NULL")
    data = dictfetchall(cur)
    print(data)
    context = {
        # 'take':take_day,
        # 'rec':rec_day,
        # 'ser':ser
        'data': data
    }
    return render(request, 'pages/show_done_not_yet_return.html', context) 


def show_untouch_shoes(request):
    cur.execute("select r.taken_day, r.receipt_id, s.service_id from receipt r, _services s where r.receipt_id = s.receipt_id and s.status is NULL")
    # data = cur.fetchall()
    data = dictfetchall(cur)
    # take_day = []
    # rec_day = []
    # ser = []
    # for da in data:
    #     take_day.append(da[0]) 
    #     rec_day.append(da[1])
    #     ser.append(da[2])
    print(data)

    context = {
        # 'take':take_day,
        # 'rec':rec_day,
        # 'ser':ser
        'data': data
    }
    return render(request, 'pages/show_untouch_shoes.html', context) #ong co the test truoc khi dua vao home sang web di LD


def show_order_in_a_day(request,day,month,year):
    cur.execute("	select * from receipt r where extract(day from r.taken_day) = '%s' and extract(month from r.taken_day) = '%s' and extract(year from r.taken_day) = '%s'"% day, month, year)
    data = cur.fetchall()
    context = {
        'data' : data
    }
    return render(request, 'pages/home.html', context)

# kết thúc ở đây
#
# def update_return_day(request, receipt_id, service_id):
#     cur.execute("update _services set return_day = current_date where receipt_id = '20122019002' and service_id = '1'")
#     conn.commit()
#     return render(request, 'pages/update_return_day.html',{'form':form)
#
def contact(request):
    return render(request, 'pages/contact.html')

def login(request):
    form = loginForm()
    if request.method == 'POST':
        # type = request.POST['type']
        form = loginForm(request.POST)
        if form.is_valid():
            type = form.clean_type()
            if type == '0':
                return render(request, 'pages/cashier.html',{'form':form,'username':form.clean_username,'thong_bao':'TC'})
            if type == '1':
                return render(request,"pages/worker.html",{'form':form,'username':form.clean_username})
    return render(request,'pages/login.html',{'form':form})

# def update_return_date(request):
#     form = update_return
def receipt(request):
    form = receipt_in()
    if request.method == 'POST':
        form = receipt_in(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'pages/cashier.html',{'form':form})
    return render(request,'pages/re_in.html',{'form':form,'thong_bao':'ma hoa don da ton tai'})

def service(request):
    form = service_in()
    if request.method == 'POST':
        form = service_in(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'pages/cashier.html',{'form':form})
    return render(request,'pages/se_in.html',{'form':form,'thong_bao':'khong thanh cong'})




def search_cus_phone(request):

    context = {}
    form = search_cus_data_phone_num()
    if request.method == 'POST':
        form = search_cus_data_phone_num(request.POST)
        if form.is_valid():       
            return render(request, 'pages/search_cus_data_phone_num.html', context)
        return render(request,'pages/search_cus_data_phone_num.html',{'form':form,})

#   # take_day = []
#     # rec_day = []
#     # ser = []
#     # for da in data:
#     #     take_day.append(da[0]) 
#     #     rec_day.append(da[1])
#     #     ser.append(da[2])
#     print(data)

#     context = {
#         # 'take':take_day,
#         # 'rec':rec_day,
#         # 'ser':ser
#         'data': data
#     }