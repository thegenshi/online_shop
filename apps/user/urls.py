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
from apps.user.views import CreateUserView, login, logout, UserProfileView, EmailVerificationView

urlpatterns = [
    path('registration/', CreateUserView.as_view(), name='registration'),
    path('login/', login, name='login'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='verify'),
    path('logout/', logout, name='logout'),
    path('profil/<int:pk>', UserProfileView.as_view(), name='profil'),
]