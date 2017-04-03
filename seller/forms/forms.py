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
    nombre = forms.CharField()
    precio = forms.DecimalField()
    imagen = forms.URLField(required=False)
    ingredientes = forms.CharField()
    categorias = forms.ModelMultipleChoiceField(queryset=Category.objects.none(), required=True,
                                                widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if pk:
            self.local = Local.objects.get(pk=pk)
            self.fields['categorias'].queryset = self.local.category_set.all()

    def createProduct(self):
        result = Product(name=self.cleaned_data['nombre'],
                         price=self.cleaned_data['precio'],
                         picture=self.cleaned_data['imagen'],
                         ingredients=self.cleaned_data['ingredientes'],
                         local=self.local)
        result.save()
        for category in self.cleaned_data["categorias"]:
            result.category.add(category)

        return result



    class Meta:
        model = Product
        fields = ('nombre', 'precio', 'categorias', 'ingredientes', 'imagen')
