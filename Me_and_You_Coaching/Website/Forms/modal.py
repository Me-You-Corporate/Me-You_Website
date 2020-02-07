from django import forms


class ModalForm(forms.Form):
    email = forms.EmailField(label='Votre e-mail',
                             widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail'}))

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if not data:
            raise forms.ValidationError("Vous devez saisir votre e-mail.")
        return data

