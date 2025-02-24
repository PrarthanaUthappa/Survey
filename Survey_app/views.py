from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import uuid
import random
import string
from .models import Expense, Form
from .forms import FormLink

# Access control for admins
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def review_expenses(request):
    expenses = Expense.objects.filter(status="Pending")
    return render(request, "review_expenses.html", {"expenses": expenses})

@login_required
@user_passes_test(is_admin)
def approve_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.status = "Approved"
    expense.save()
    send_expense_email(expense.recipient_email, "Approved", "N/A")
    return redirect("review_expenses")

@login_required
@user_passes_test(is_admin)
def reject_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.status = "Rejected"
    expense.save()
    send_expense_email(expense.recipient_email, "Rejected", "N/A")
    return redirect("review_expenses")

@login_required
@user_passes_test(is_admin)
def Survey_email(request):
    if request.method == "POST":
        form = FormLink(request.POST)
        if form.is_valid():
            Email = form.cleaned_data["Email"]
            form_link = f"http://127.0.0.1:8000/fill_form/{uuid.uuid4()}"
            Form.objects.create(Email=Email, Link=form_link)
            send_expense_email(Email, "Submitted", form_link)
            messages.success(request, "Form link sent successfully!")
            return redirect("send_email")
    else:
        form = FormLink()
    return render(request, "Survey_app/send_mail.html", {"form": form})

@login_required
def submit_expense(request, Unique_id):
    form_entry = get_object_or_404(Form, Link=f"http://127.0.0.1:8000/fill_form/{Unique_id}")
    if request.method == "POST":
        form_entry.tea_expense = float(request.POST.get("tea", 0))
        form_entry.coffee_expense = float(request.POST.get("coffee", 0))
        form_entry.smoking_expense = float(request.POST.get("smoking", 0))
        form_entry.biscuit_expense = float(request.POST.get("biscuit", 0))
        form_entry.isapprove = False
        form_entry.save()
        send_expense_email(form_entry.Email, "Submitted", form_entry.Link)
        messages.success(request, "Expense submitted successfully! Awaiting admin approval.")
        return redirect("success_page")
    return render(request, "Survey_app/fill_form.html", {"form_entry": form_entry})

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    forms = Form.objects.all()
    return render(request, "Survey_app/dashboard.html", {"forms": forms})

@login_required
@user_passes_test(is_admin)
def approve(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if not form.isapprove:
        form.Password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        form.isapprove = True
        form.save()
        send_expense_email(form.Email, "Approved", form.Link)
    return redirect("dashboard")

def send_expense_email(user_email, status, form_link):
    subject = f"Expense Form - {status}"
    messages = {
        "Submitted": f"Hello,\n\nYour expense form has been successfully submitted. It is currently under review.\n\nYou can track it here: {form_link}\n\nBest regards,\nAdmin",
        "Approved": f"Hello,\n\nYour expense form has been approved! You can check your details here: {form_link}\n\nBest regards,\nAdmin",
        "Rejected": f"Hello,\n\nUnfortunately, your expense form has been rejected. Please contact the admin for further details.\n\nBest regards,\nAdmin"
    }
    send_mail(subject, messages[status], settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

@login_required
def dashboard_user(request, form_id):
    form = get_object_or_404(Form, id=form_id, isapprove=True)
    amount_spent_per_day = (form.tea_expense or 0) + (form.coffee_expense or 0) + (form.smoking_expense or 0) + (form.biscuit_expense or 0)
    after_analysis = {
        "daily": amount_spent_per_day,
        "weekly": amount_spent_per_day * 7,
        "monthly": amount_spent_per_day * 30,
    }
    return render(request, "Survey_app/dashboard.html", {"form": form, "after_analysis": after_analysis})
