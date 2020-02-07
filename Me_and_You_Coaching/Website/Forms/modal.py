from django import forms


class ModalForm(forms.Form):
    email = forms.CharField(label='Votre e-mail')