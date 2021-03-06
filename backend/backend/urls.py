"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import debug_toolbar
from core import views

# router = routers.DefaultRouter()                   
# router.register(r'customers', views.CustomerView, 'customer')
# router.register(r'accounts', views.AccountView, 'account')
# router.register(r'transactions', views.TransactionView, 'transaction')  

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    path('api/', include('core.urls')),
    path('api/', include('jsonrpc_app.urls')),
    path('playground/', include('playground.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
