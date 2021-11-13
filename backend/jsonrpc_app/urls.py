from django.urls import path
from . import views

urlpatterns = [
    path('jsonrpc/', views.JsonRpcApp.as_view())
]