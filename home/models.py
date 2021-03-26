# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Services(models.Model):
    service_id = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    description = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    request = models.CharField(max_length=50, blank=True, null=True)
    return_day = models.DateField(blank=True, null=True)
    receipt = models.OneToOneField('Receipt', models.DO_NOTHING, primary_key=True)
    worker = models.ForeignKey('Worker', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = '_services'
        unique_together = (('receipt', 'service_id'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cashier(models.Model):
    cashier_id = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=10)
    address = models.CharField(max_length=50, blank=True, null=True)
    num_of_work_days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cashier'


class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=10)
    sex = models.CharField(max_length=1, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Receipt(models.Model):
    receipt_id = models.CharField(primary_key=True, max_length=11)
    taken_day = models.DateField()
    cashier = models.ForeignKey(Cashier, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    taken_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'receipt'


class Schedule(models.Model):
    date = models.DateField()
    cashier_id = models.CharField(primary_key=True, max_length=15)

    class Meta:
        managed = True
        db_table = 'schedule'


class Worker(models.Model):
    worker_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone_num = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'worker'
    def __str__(self):
        return self.worker_id
    def worker_name(self):
        return self.name
    def worker_dob(self):
        return ', '.join(self.dob)
    def worker_address(self):
        return ', '.join(self.address)
    def worker_phone_num(self):
        return self.phone_num

