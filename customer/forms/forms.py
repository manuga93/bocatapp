from django import forms


class OrderLineDoneForm(forms.Form):
    status = forms.BooleanField(required=True, widget=forms.CheckboxInput)
