from django import forms
from django.core.exceptions import ValidationError

from datetime import date


class DollarForm(forms.Form):

    start_date = forms.DateField(
        label='Fecha inicial',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label='Fecha final',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and not start_date < end_date:
            raise ValidationError(
                'La fecha inicial debe ser menor a la fecha final.')

        if start_date.year < 1954:
            raise ValidationError(
                'La fecha inicial no puede ser menor a 1954.'
            )

        if end_date and end_date.year < 1954:
            raise ValidationError(
                'La fecha final no puede ser menor a 1954.'
            )

        if end_date and end_date > date.today():
            raise ValidationError(
                'La fecha final no puede ser mayor a la fecha actual')
