from apps.user.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'login-input' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'login-input' }))
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    email= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите электронную почту','class':'login-input', 'type':'email'}))
    password1= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    password2= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Потвердите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'form-control' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'form-control' }))
    image= forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' }), required=False)
    email= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите электронную почту','class':'form-control', 'readonly':True}))
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'form-control', 'readonly':True}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')