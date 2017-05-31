from django import forms
from django.core.exceptions import ValidationError
from seller.models import Pack, Local
import datetime
from django.utils.translation import ugettext_lazy as _

class PackForm(forms.ModelForm):
    nombre = forms.CharField()
    precio = forms.DecimalField()
    fecha_fin = forms.DateField(input_formats=['%d/%m/%Y'], initial=datetime.date.today)
    fecha_fin.widget.format = '%d/%m/%Y'
    fecha_fin.widget.attrs['class'] = u'dateinput'
    imagen = forms.URLField(required=False)
    fecha_inicio = datetime.date.today()

    class Meta:
        model = Pack
        fields = ['nombre', 'precio', 'fecha_fin', 'imagen']

    def create(self, local_pk):
        local = Local.objects.get(pk=local_pk)
        result = Pack(name=self.cleaned_data['nombre'],
                      price=self.cleaned_data['precio'],
                      photo=self.cleaned_data['imagen'],
                      initDate=self.fecha_inicio,
                      endDate=self.cleaned_data['fecha_fin'],
                      local=local)

        return result

    def clean(self):
        if not self.data['fecha_fin']:
            raise ValidationError(_('You must enter a valid date'))
        if self.fecha_inicio > self.cleaned_data['fecha_fin']:
            raise ValidationError(_('You must enter a date in the future'))
        if len(self.data['precio']) == 0:
            raise ValidationError(_('Enter a price!'))
        else:
            if int(self.data['precio']) <= 0:
                raise ValidationError(_('Too cheap!'))