from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255, null=True)
    address_line_2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2, default='US')
    zip_code = models.CharField(max_length=255)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True)
    
    def _str_(self):
         return self.first_name + ' ' + self.last_name
    

class Account(models.Model):
    account_hash = models.CharField(max_length=1024)
    bitcoin_balance = models.DecimalField(max_digits=12,decimal_places=8)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Transaction(models.Model):
    bitcoin_value = models.DecimalField(max_digits=12,decimal_places=8)
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='from_account')
    to_account = models.ForeignKey(Account,on_delete=models.PROTECT, related_name='to_account')
