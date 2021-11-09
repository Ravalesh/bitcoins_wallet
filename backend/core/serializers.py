import json
from django.db.models import fields
from django.contrib.auth import models as UserModel
from rest_framework import serializers
from decimal import Decimal
from .models import Customer, Account, Transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'address_line_1', 'address_line_2', 'city', 'state', 'country_code', 
        'zip_code')
    
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_hash', 'bitcoin_balance', 'customer')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'bitcoin_value', 'from_account', 'to_account')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel.User
        fields = ('username', 'password')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)