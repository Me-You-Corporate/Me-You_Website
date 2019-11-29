from django import forms

MIN_SIZE = 8


class SignupForm(forms.Form):
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

    password_rules = [
        lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
        lambda s: any(x.islower() for x in s),  # must have at least one lowercase
        lambda s: any(x.isdigit() for x in s),  # must have at least one digit
        lambda s: len(s) >= MIN_SIZE  # must be at least MIN_SIZE characters
        ]

    def clean_email_confirm(self, *args, **kwargs):
        email_confirm = self.cleaned_data.get('email_confirm')
        email = self.cleaned_data.get('email')

        if email == email_confirm:
            return email_confirm
        raise forms.ValidationError('Your confirmation doesn\'t match your email.')

    def clean_password_confirm(self, *args, **kwargs):
        password_confirm = self.cleaned_data.get('password_confirm')
        password = self.cleaned_data.get('password')

        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError('Your confirmation doesn\'t match your password.')

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        if all(rule(password) for rule in SignupForm.password_rules):
            return password
        errors = []
        if not any(x.isupper() for x in password):
            errors.append('Your password needs at least 1 capital.')
        if not any(x.islower() for x in password):
            errors.append('Your password needs at least 1 lowecarse.')
        if not any(x.isdigit() for x in password):
            errors.append('Your password needs at least 1 number.')
        if len(password) < 8:
            errors.append('Your password needs to be at least 8 characters.')
        raise forms.ValidationError(errors)
