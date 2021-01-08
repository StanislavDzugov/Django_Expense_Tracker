from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'amountField',
        'type': 'number'
    }))
    date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'dateField',
        'type': 'date'
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'descriptionField',
    }))
    source = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'categoryField',
        'list': 'datalistOptions',
    }))

    class Meta:
        model = Income
        fields = ['amount', 'date', 'description', 'owner', 'source']
