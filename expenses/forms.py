from .models import Expense
from django import forms


class ExpenseForm(forms.ModelForm):
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
    category = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'categoryField',
        'list': 'datalistOptions',
    }))

    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'owner', 'category']

