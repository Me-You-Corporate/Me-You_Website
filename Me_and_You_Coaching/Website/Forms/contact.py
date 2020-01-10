from django import forms

class ContactForm(forms.Form):
    username = forms.CharField(label='Votre nom')
    email = forms.CharField(label='Votre e-mail')
    subject = forms.CharField(label='Sujet')
    message = forms.CharField(widget=forms.Textarea, label='Message')

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if not data:
            raise forms.ValidationError("Vous devez saisir votre e-mail.")
        return data
