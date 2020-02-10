from django import forms
from ..models import User

MIN_SIZE = 8

#on save user : email is in email table with user ID accordingly generated
#first last, password, time created & path to documents in user table
#send email confirm & save documents to given path; if exist
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    # maybe get first name, last name, etc
    identification_document = forms.FileField(required=False)
    # maybe get first name, last name & number // check against ID
    professional_document = forms.FileField(required=False)

    #in order to generate user ID
    zipcode = forms.CharField()
    #once userID is generated & login works + other stuff
    #inser laposte_hexasmal.csv in DB then feth table to find if zipcode exists

    password_rules = [
        lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
        lambda s: any(x.islower() for x in s),  # must have at least one lowercase
        lambda s: any(x.isdigit() for x in s),  # must have at least one digit
        lambda s: len(s) >= MIN_SIZE  # must be at least MIN_SIZE characters
        ]

    def clean_email_confirm(self, *args, **kwargs):
        email_confirm_ = self.cleaned_data.get('email_confirm')
        email_ = self.cleaned_data.get('email')

        if email_ == email_confirm_:
            return email_confirm_
        raise forms.ValidationError('Les e-mails que vous avez saisi ne correspondent pas.')

    def clean_password_confirm(self, *args, **kwargs):
        password_ = self.cleaned_data.get('password')
        password_confirm_ = self.cleaned_data.get('password_confirm')

        if all(rule(password_) for rule in SignupForm.password_rules):
            return password_
        errors = []
        if not any(x.isupper() for x in password_):
            errors.append('Votre mot de passe requiert au moins une majuscule.')
        if not any(x.islower() for x in password_):
            errors.append('Votre mot de passe requiert au moins une minuscule.')
        if not any(x.isdigit() for x in password_):
            errors.append('Votre mot de passe requiert au moins un chiffre.')
        if len(password_) < 8:
            errors.append('Votre mot de passe requiert au moins huit characteres.')
        if password_confirm_ != password_:
            errors.append('Les mots de passe que vous avez saisis ne correspondent pas.')
        raise forms.ValidationError(errors)
