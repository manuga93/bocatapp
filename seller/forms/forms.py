from django import forms
from ..models import Local, Category, Product


class LocalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocalForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['description'].label = "Descripcion"
        self.fields['address'].label = "Direccion"
        self.fields['phone'].label = "Telefono"
        self.fields['postalCode'].label = "Codigo Postal"
        self.fields['photo'].label = "Foto"

    class Meta:
        model = Local
        fields = ('name', 'description', 'address', 'phone', 'postalCode', 'photo')


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['description'].label = "Descripcion"

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
