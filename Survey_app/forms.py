
from django import forms
from .models import Form  # Import the correct model

class FormModelForm(forms.ModelForm):
    class Meta:
        model = Form  # Make sure this matches your model
        fields = ["Email"]  # Use "Email" with capital 'E' to match the model

class ExpenseForm(forms.Form):
    tea_expense = forms.DecimalField(label="Tea Expense ($)", required=False, min_value=0)
    coffee_expense = forms.DecimalField(label="Coffee Expense ($)", required=False, min_value=0)
    biscuit_expense = forms.DecimalField(label="Biscuit Expense ($)", required=False, min_value=0)
    smoking_expense = forms.DecimalField(label="Smoking Expense ($)", required=False, min_value=0)
    groceries_expense = forms.DecimalField(label="Groceries Expense ($)", required=False, min_value=0)




