from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Register(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Введіть, будь ласка, електронну пошту.')
    first_name = forms.CharField(max_length=15, required=True, help_text='Ваше ім`я')
    last_name = forms.CharField(max_length=20, required=False, help_text='Ваше прізвище')
    date_of_birth = forms.DateField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']