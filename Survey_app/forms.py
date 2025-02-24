from django import forms
from .models import Form

class FormLink(forms.ModelForm):
    class Meta:
        model = Form
        fields = ["Email", "Link"]




class ExpenseForm(forms.Form):
    tea_expense = forms.DecimalField(label="Tea Expense", required=True)
    coffee_expense = forms.DecimalField(label="Coffee Expense", required=True)
    biscuit_expense = forms.DecimalField(label="Biscuit Expense", required=True)
    smoking_expense = forms.DecimalField(label="Smoking Expense", required=True)
