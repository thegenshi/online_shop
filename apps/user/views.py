from django.shortcuts import render
from apps.user.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались на нашем сайте')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render (request, 'registration.html', {'form':form})



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('profil'))
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})

def logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/')

@login_required(login_url="login")
def profil(request):
    if request.method == 'POST':
        form = UserProfileForm(data = request.POST, instance = request.user, files = request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profil'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance = request.user)
    context = {'form':form}
    return render(request, 'profil.html', context)

