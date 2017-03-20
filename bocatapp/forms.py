from django import forms
from models import User, Profile


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']


class UserForm(forms.ModelForm):
    first_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class UserProfileForm(forms.ModelForm):
    phone = forms.RegexField(required=False, regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                                 "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'avatar']
