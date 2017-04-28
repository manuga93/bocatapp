# -*- coding: utf-8 -*-
from django import forms
from models import User, Profile


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo"
        self.fields['password'].label = "Contraseña"

    def create_user(self):
        res = User(first_name=self.cleaned_data['username'],
                   email=self.cleaned_data['first_name'],
                   username=self.cleaned_data['last_name'],
                   password=self.cleaned_data['email'],
                   last_name=self.cleaned_data['password'])
        return res

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class UserForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo"

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    phone = forms.PhoneField()
    birth_date = forms.CharField(required=False)
    avatar = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].label = "Teléfono"
        self.fields['birth_date'].label = "Cumpleaños"
        self.fields['avatar'].label = "Avatar"

    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'avatar']
