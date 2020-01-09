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
        email_confirm_ = self.cleaned_data.get('email_confirm')
        email_ = self.cleaned_data.get('email')

        if email_ == email_confirm_:
            return email_confirm_
        raise forms.ValidationError('Your confirmation doesn\'t match your email.')

    def clean_password_confirm(self, *args, **kwargs):
        password_confirm_ = self.cleaned_data.get('password_confirm')
        password_ = self.clean_password()

        if password_ == password_confirm_:
            return password_confirm_
        raise forms.ValidationError('Your confirmation doesn\'t match your password.')

    def clean_password(self, *args, **kwargs):
        password_ = self.cleaned_data.get('password')
        print('|')
        print(password_)
        print('|')
        if all(rule(password_) for rule in SignupForm.password_rules):
            return password_
        errors = []
        if not any(x.isupper() for x in password_):
            errors.append('Your password needs at least 1 capital.')
        if not any(x.islower() for x in password_):
            errors.append('Your password needs at least 1 lowecarse.')
        if not any(x.isdigit() for x in password_):
            errors.append('Your password needs at least 1 number.')
        if len(password_) < 8:
            errors.append('Your password needs to be at least 8 characters.')
        raise forms.ValidationError(errors)
