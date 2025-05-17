from django import forms
from .models import Trip, Participant, Expense


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name']


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'paid_by', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
