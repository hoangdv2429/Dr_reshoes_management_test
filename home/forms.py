from home.models import Cashier
from typing import no_type_check
from django import forms
from django.http import request
from django.shortcuts import redirect
import psycopg2
import re

conn = psycopg2.connect(database = 'shoes_spa',user = 'postgres',password ='admin',host='localhost',port='5432') #ket noi vao database = conn
cur = conn.cursor() #con tro du lieu... lam viec o da
cur.execute("select cashier_id from cashier")
data = cur.fetchall()
user=[]

for row in data:
    user.append(row[0])
#
cur.execute("select worker_id from worker")
data1 = cur.fetchall()

for row in data1:
    user.append(row[0])
#
def check_user(username):
    i = 0
    for users in user:
        if username == users:
            i+=1
    if i == 0:
        return False
    else:
        return True
#
def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
#

class loginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập',max_length=30)
    password = forms.CharField(label='Mật khẩu',widget = forms.PasswordInput())
    type = forms.ChoiceField(label="Là", choices =(('0','cashier'),('1','worker')))
    #
    #
    def clean_type(self):
        return type
    def clean_username(self):
            username = self.cleaned_data['username']
            if not re.search(r'^\w+$', username):
                raise forms.ValidationError("Tên đăng nhập có ký tự đặc biệt.")
            if check_user(username) == False:
                raise forms.ValidationError("Tài khoản này không tồn tại.")
            else:
                return username

    def clean_password(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if check_user(username) == False:
                raise forms.ValidationError("Tài khoản không tồn tại.")
            else:
                if password != '1234':
                    raise forms.ValidationError("Sai mật khẩu")
                else:
                    return password   
    def clean_type(self):
        type = self.cleaned_data['type']
        return type


# cur.execute("select receipt_id, service_id from _services")
# data2 = cur.fetchall()
# receipt_id=[]
# service_id=[]

# for row in data2:
#     receipt_id.append(row[0])
#     service_id.append(row[1])

cur.execute("select receipt_id from receipt")
data1 = cur.fetchall()
receipt_id = []
for row in data1:
    receipt_id.append(row[0])
#
def check_receipt(receipt_id_in):
    i = 0
    for receipt_ids in receipt_id:
        if receipt_id_in == receipt_ids:
            i+=1
    if i == 0:
        return False
    else:
        return True


class receipt_in(forms.Form):
    receipt_id = forms.CharField(label='id hoá đơn',max_length = 30)
    # taken_day = forms.CharField(label='ngày nhập hoá đơn') lấy bằng current date
    cashier_id = forms.CharField(label='mã nv thu ngân', max_length= 10)
    cus = forms.CharField(label='mã khách hàng', max_length= 10)
    def save(self):
        
        if check_receipt(self.cleaned_data['receipt_id']) == True:
            raise forms.ValidationError("id da ton tai.")
        if check_receipt(self.cleaned_data['receipt_id']) == False:
            cur.execute("insert into receipt values('%s',current_date,'%s','%s')" % (self.cleaned_data['receipt_id'],self.cleaned_data['cashier_id'],self.cleaned_data['cus']))
            conn.commit()

class service_in(forms.Form):
    service_id = forms.CharField(label='id dịch vụ', max_length=4)
    price = forms.CharField(label='giá', max_length=10)
    request = forms.CharField(label='yêu cầu', max_length= 100)
    cashier_id = forms.CharField(label='id người nhập hoá đơn: ', max_length=11)
    def save(self):
            cur.execute("insert into services(service_id, price,request,cashier_id) values('%s','%s','%s','%s')" % (self.cleaned_data['service_id'],self.cleaned_data['price'],self.cleaned_data['request'],self.cleaned_data['cashier_id']))
            conn.commit()    


class search_cus_data_phone_num(forms.Form):
    phone_num = forms.CharField(label='số điện thoại',max_length = 11)

    def search(self):
        cus_id = []
        cur.execute("select customer_id from customer where phone_number = '%s'" % (self.cleaned_data['phone_num']))
        data = cur.fetchall()
        for da in data:
            cus_id.append(row[0])
        context = { 
                'cus_id': cus_id   
            }     
        return context

