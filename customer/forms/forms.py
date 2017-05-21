from django import forms
from ..models import Comment, Report


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = "Descripcion"
        self.fields['rating'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ('description', 'rating')


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['reason'].label = "Razon"

    class Meta:
        model = Report
        fields = ('reason',)


class RechargeForm(forms.Form):
    amount = forms.DecimalField(min_value=10, max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(RechargeForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = "Cantidad a recargar"

    class Meta:
        fields = ('amount',)
