from django import forms
from ..models import Local, Category, Product


class LocalForm(forms.ModelForm):

    class Meta:
        model = Local
        fields = ('name', 'description', 'address', 'phone', 'photo')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'description')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'local', 'ingredients', 'picture')