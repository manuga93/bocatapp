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
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'avatar']
