from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail', required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail'}))
    password = forms.CharField(label='Mot de passe', required=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if not data:
            raise forms.ValidationError("Vous devez saisir votre e-mail.")
        return data
