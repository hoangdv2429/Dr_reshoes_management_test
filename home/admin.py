from django.contrib import admin

# Register your models here.
from .models import Cashier, Worker, Customer, Services

admin.site.register(Worker)
admin.site.register(Cashier)
admin.site.register(Customer)
admin.site.register(Services)
