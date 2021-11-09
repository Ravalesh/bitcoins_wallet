from django.shortcuts import render
from django.http import HttpResponse
from core.models import Customer
from core.serializers import DecimalEncoder

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
def lets_play(request):
    try:
        customer = Customer.objects.select_related('account').values('id', 'first_name', 'last_name', 
        'account__account_hash', 'account__bitcoin_balance') \
        .filter(user__id=1).first()
        if customer is not None:
            return render(request, 'hello.html', {'name': 'Mosh', 'customers': customer})
        else:
            return HttpResponseNotFound("Customer not found")
    except Exception as e:
        return HttpResponseError(e)
     
