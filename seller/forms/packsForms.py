from django import forms
from seller.models import Pack


class PackForm(forms.ModelForm):
    name = forms.CharField()
    price = forms.DecimalField()
    endDate = forms.DateField(input_formats=['%d/%m/%Y'])
    endDate.widget.format = '%d/%m/%Y'
    endDate.widget.attrs['class'] = u'dateinput'
    photo = forms.URLField(required=False)

    class Meta:
        model = Pack
        fields = ['name', 'price', 'endDate', 'photo']
