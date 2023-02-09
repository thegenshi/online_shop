from django.shortcuts import render
from apps.user.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from apps.user.models import User, EmailVerification
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались на нашем сайте')
#             return HttpResponseRedirect(reverse('login'))
#     else:
#         form = UserRegistrationForm()
#     return render (request, 'registration.html', {'form':form})

class CreateUserView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    def get_context_data(self, **kwargs):
        context =  super(CreateUserView, self).get_context_data(**kwargs)
        return context



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})

def logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/')

class UserProfileView(UpdateView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('base')
    fields = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        return context

class EmailVerificationView(TemplateView):
    template_name = 'verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email = kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code = code)
        if email_verification.exists():
            user.is_confirm_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')