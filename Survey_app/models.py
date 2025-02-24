from django.db import models

class Form(models.Model):
    Email=models.EmailField()
    Created_Time=models.DateTimeField(auto_now_add=True)
    Link =models.URLField()
    tea_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    coffee_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    biscuit_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    smoking_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    approve=models.BooleanField(default=False)
    Password=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self): 
        return f"form submitted by {self.Email} -{'Approved' if self.approve else 'Pending'}"
    
class Expense(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
