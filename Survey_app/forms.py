from django import forms

class ExpenseForm(forms.Form):
    tea_expense = forms.DecimalField(label="Tea Expense ($)", required=False, min_value=0)
    coffee_expense = forms.DecimalField(label="Coffee Expense ($)", required=False, min_value=0)
    biscuit_expense = forms.DecimalField(label="Biscuit Expense ($)", required=False, min_value=0)
    smoking_expense = forms.DecimalField(label="Smoking Expense ($)", required=False, min_value=0)
    groceries_expense = forms.DecimalField(label="Groceries Expense ($)", required=False, min_value=0)




