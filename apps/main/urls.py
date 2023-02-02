"""electronics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from apps.main.views import main, info, add_to_cart, cart, remove, search, category, contact_us

urlpatterns = [
    path('', main, name='main'),
    path('info/<int:id>', info, name='info'),
    path('add_to_cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('search/', search, name='search'),
    path('contact_us/', contact_us, name='contact_us'),
    path('remove/<int:id>', remove, name='remove'),
    path('category/<slug:slug>', category, name='category'),
]
