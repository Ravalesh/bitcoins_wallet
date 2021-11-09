from django.contrib import admin
from .models import Customer,Account
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list = ('first_name', 'last_name', 'address_line_1', 'address_line_2', 'city', 'state', 'country_code', 
    'zip_code')

class AccountAdmin(admin.ModelAdmin):
    list = ('account_hash', 'bitcoin_balance', 'customer')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Account, AccountAdmin)