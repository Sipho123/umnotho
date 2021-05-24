from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import Accounts




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountsAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Accounts
        fields = ('email', 'password')
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Accounts
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(email=email)
            except account.DoesNotExist:

                return email
            raise forms.ValidationError(
                "Email '%s' is already in use." % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except account.DoesNotExist:
                return username
            raise forms.ValidationError(
                "Username '%s' is already in use." % username)
