from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail')
    password = forms.CharField(widget=forms.PasswordInput())
