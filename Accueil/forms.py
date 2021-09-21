from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form, UserCreationForm):

 username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':"nom d'utilisateur"}))
 email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':"l'adresse e-mail"}))
 password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':"mot de passe"}))
 password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':"Confimer mot de passe"}))
 


 def clean_username(self):
    username = self.cleaned_data.get('username')
    if User.objects.filter(username__iexact=username).exists():
        raise forms.ValidationError('Username already exists')
    return username

 def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email__iexact=email).exists():
        raise forms.ValidationError('A user has already registered using this email')
    return email

 def clean_password2(self):
    '''
    we must ensure that both passwords are identical
    '''
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError('Passwords must match')
    return password2