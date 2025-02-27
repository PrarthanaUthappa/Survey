from django.db import models
import uuid
class Form(models.Model):
    Email = models.EmailField(blank=True, null=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    Created_Time=models.DateTimeField(auto_now_add=True)
    Link = models.CharField(max_length=255, unique=True)  
    tea_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    coffee_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    biscuit_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    smoking_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    isapprove=models.BooleanField(default=False)
    Password=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self): 
        return f"form submitted by {self.Email} -{'Approved' if self.isapprove else 'Pending'}"
    
class Expense(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
