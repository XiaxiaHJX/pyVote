

from django import forms

class loginForm(forms.Form):
    username=forms.CharField(min_length=5,max_length=10,required=True,widget=forms.TextInput)
    password=forms.CharField(min_length=5,max_length=10,required=True,widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    pass