from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('authenticate/', csrf_exempt(views.authenticate_user)), #post
    path('logout/', csrf_exempt(views.logout_user)), #get
    path('profile/', csrf_exempt(views.get_customer_profile)), #get
    path('send/', csrf_exempt(views.send_bitcoins)), #post
]

