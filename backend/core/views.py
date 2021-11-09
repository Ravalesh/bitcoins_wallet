from decimal import Decimal
import io
import json
from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .serializers import CustomerSerializer, AccountSerializer, TransactionSerializer, DecimalEncoder
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Account, Transaction

class HttpResponseSuccess(HttpResponse):
    status_code = 200

class HttpResponseAccessDenied(HttpResponse):
    status_code = 401

class HttpResponseInactiveUser(HttpResponse):
    status_code = 403

class HttpResponseError(HttpResponse):
    status_code = 500

class HttpResponseNotFound(HttpResponse):
    status_code = 404

# Create your views here.
class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated,]

class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated,]

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated,]

# class UserView(APIView):

#     serializer_class = UserSerializer
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     return HttpResponseSuccess()
#                 else:
#                     return HttpResponseInactiveUser()
#             else:
#                 return HttpResponseError()

@require_http_methods(["POST"])
def authenticate_user(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            response_string = {}
            response_string['id'] = user.id
            response_string['name'] = user.username
            return HttpResponseSuccess(json.dumps(response_string), content_type="application/json")
        else:
            return HttpResponseInactiveUser()
    else:
        return HttpResponseAccessDenied()

def logout_user(request):
    logout(request)
    return HttpResponseSuccess()


def get_customer_profile(request):
    try:
        # if not request.user.is_authenticated:
        #      return HttpResponseAccessDenied()
        id = request.GET.get('id')
        if id:
            customer = Customer.objects.select_related('account').values('id', 'first_name', 'last_name', 
            'account__account_hash', 'account__bitcoin_balance') \
            .filter(user__id=id).first()
            if customer is not None:
                response_string = {}
                response_string['id'] = customer['id']
                response_string['first_name'] = customer['first_name']
                response_string['last_name'] = customer['last_name']
                response_string['account_hash'] = customer['account__account_hash']
                response_string['bitcoin_balance'] = json.dumps(customer['account__bitcoin_balance'], 
                cls=DecimalEncoder)
                return HttpResponseSuccess(json.dumps(response_string), 
                content_type="application/json")
            else:
                return HttpResponseNotFound("Customer not found")
        else:
            return HttpResponseNotFound("Customer not found")
    except Exception as e:
        return HttpResponseError(e)

@require_http_methods(["POST"])
def send_bitcoins(request):
    try:
        # if not request.user.is_authenticated:
        #      return HttpResponseAccessDenied()
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        from_id=data['from_customer_id']
        to_address = data['to_address']
        amount = Decimal(data['amount'])
        if from_id and to_address and amount:
            #check if the customer has enough bitcoins
            customer = Customer.objects.select_related('account').values('account__bitcoin_balance') \
            .filter(user__id=from_id).first()
            if customer is not None and customer['account__bitcoin_balance'] < amount:
                return HttpResponseError('Insufficient balance')
            #get the to account ID
            customer = Customer.objects.select_related('account').values('account__id') \
            .filter(account__account_hash=to_address).first()
            if customer is not None:
                with transaction.atomic():
                    #create a transaction record
                    bitcoin_transaction = Transaction()
                    bitcoin_transaction.bitcoin_value = amount
                    bitcoin_transaction.from_account_id = from_id
                    bitcoin_transaction.to_account_id = customer['account__id']
                    bitcoin_transaction.save()

                    #update the balances in account table
                    bitcoin_account = Account.objects.get(pk=from_id)
                    bitcoin_account.bitcoin_balance = bitcoin_account.bitcoin_balance-amount
                    bitcoin_account.save()

                    bitcoin_account = Account.objects.get(pk=customer['account__id'])
                    bitcoin_account.bitcoin_balance = bitcoin_account.bitcoin_balance+amount
                    bitcoin_account.save()
                    response_string = {}
                    response_string['status'] = "success"
                    return HttpResponseSuccess(json.dumps(response_string), 
                    content_type="application/json")
            else:
                return HttpResponseError('Error')
        else:
             return HttpResponseError('Error')
    except Exception as e:
        return HttpResponseError(e)

