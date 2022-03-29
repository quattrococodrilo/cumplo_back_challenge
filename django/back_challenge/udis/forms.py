from cProfile import label
from django import forms


class UdisForm(forms.Form):

    start_date = forms.DateField(
        label='Fecha inicial',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label='Fecha final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
