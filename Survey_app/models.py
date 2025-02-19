from django.db import models

class Form(models.Model):
    Email=models.EmailField()
    Created_Time=models.DateTimeField(auto_now_add=True)
    Link =models.URLField()

    def __str__(self):
        return f"Survey for {self.Email} is {self.Link}"


# to store response
class Response(models.Model):
    Email=models.EmailField()
    Submitted_Time=models.DateTimeField(auto_now_add=True)
    tea_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    coffee_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    biscuit_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    smoking_expense = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"subitted by {self.Email}"