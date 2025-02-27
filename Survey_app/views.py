from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import FormModelForm,ExpenseForm # Import the form
from .models import Expense,Form 
from django.http import HttpResponseForbidden
import uuid
import random
import string 
from django.http import HttpResponse

# Access control for admins
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def review_expenses(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to review expenses.")
    expenses = Expense.objects.filter(status="Pending")
    return render(request, "review_expenses.html", {"expenses": expenses})

# @login_required
# @user_passes_test(is_admin)
# def approve_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id)
#     expense.status = "Approved"
#     expense.save()
#     send_expense_email(expense.recipient_email, "Approved", "N/A")
#     return redirect("review_expenses")

# @login_required
# @user_passes_test(is_admin)
# def reject_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id)
#     expense.status = "Rejected"
#     expense.save()
#     send_expense_email(expense.recipient_email, "Rejected", "N/A")
#     return redirect("review_expenses")

@login_required
@user_passes_test(is_admin)
def Survey_email(request):
    form=ExpenseForm()
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            Email = form.cleaned_data["Email"]
            unique_id = str(uuid.uuid4())  # Generate UUID
            form_link = f"http://127.0.0.1:8000/fill_form/{unique_id}"
            
            # Save to database
            Form.objects.create(Email=Email, Link=form_link, unique_id=unique_id)

            send_expense_email(Email, "Submitted", form_link)
            messages.success(request, "Form link sent successfully!")
            return redirect("send_email")
    return render(request, "Survey_app/send_mail.html", {"form": form})


@login_required
def submit_expense_with_id(request, unique_id):
    form_entry, created = Form.objects.get_or_create(unique_id=unique_id)

    if created:
        print(f"New Form entry created for unique_id: {unique_id}")

    if request.method == "POST":
        form_entry.tea_expense = float(request.POST.get("tea", 0))
        form_entry.coffee_expense = float(request.POST.get("coffee", 0))
        form_entry.smoking_expense = float(request.POST.get("smoking", 0))
        form_entry.biscuit_expense = float(request.POST.get("biscuit", 0))
        form_entry.isapprove = False  # Mark as pending approval
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



def admin_review_forms(request):
    pending_forms = Form.objects.filter(isapprove=False)
    return render(request, "admin_review.html", {"pending_forms": pending_forms})


# @login_required
# @user_passes_test(is_admin)
def approve_form(request):
    if request.method == "POST":
        form_id = request.POST.get("form_id")
        form_entry = get_object_or_404(Form, id=form_id)
        form_entry.approved = True
        form_entry.save()
        return redirect("admin_review_forms")
    return HttpResponse("Invalid request", status=400)

def send_expense_email(user_email, status, form_link):
    subject = f"Expense Form - {status}"
    messages = {
        "Submitted": f"Hello,\n\nYour expense form has been successfully submitted. It is currently under review.\n\nYou can track it here: {form_link}\n\nBest regards,\nAdmin",
        "Approved": f"Hello,\n\nYour expense form has been approved! You can check your details here: {form_link}\n\nBest regards,\nAdmin",
        "Rejected": f"Hello,\n\nUnfortunately, your expense form has been rejected. Please contact the admin for further details.\n\nBest regards,\nAdmin"
    }
    send_mail(subject, messages[status], settings.EMAIL_HOST_USER, [user_email], fail_silently=False)


def submit_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Process form data (e.g., save to database)
            return HttpResponse("Your expenses have been recorded!")
    else:
        form = ExpenseForm()
    
    return render(request, 'expense_form.html', {'form': form})


def fill_form(request, unique_id):
    form, created = Form.objects.get_or_create(unique_id=unique_id, defaults={"Email": "", "Password": ""})
    if request.method == "POST":
        form.Email = request.POST.get("Email")
        form.Password = request.POST.get("password")
        form.save()
        return redirect("success_page")  # Redirect after submission

    return render(request, "Survey_app/fill_form.html", {"form": form, "created": created})


 # Import the model

def submit_form(request):
    if request.method == "POST":
        form = FormModelForm(request.POST)
        print("📝 Form Data Received:", request.POST)  # Debugging output

        if form.is_valid():
            form_entry = form.save(commit=False)
            print("✅ Captured Email Before Save:", form_entry.Email)  # Debug Email
            form_entry.save()
            print("💾 Form saved successfully!")
            return redirect("success")  # Redirect to success page
        else:
            print("❌ Form Errors:", form.errors)  # Debug validation errors

    else:
        form = FormModelForm()
    return render(request, "form_template.html", {"form": form})


def success_page(request):
    return render(request, "Survey_app/success.html")



def send_invite_email(request):
    form = FormModelForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        recipient_email = form.cleaned_data["Email"]  # Get user email
        unique_id = str(uuid.uuid4())  
        form_link = request.build_absolute_uri(f"/fill_form/{unique_id}/")

        subject = "Fill Out Your Daily Expenses"
        message = f"""
        Hello,

        You have to submit the following expenses for approval:
        
        Please fill out the form by clicking the link below:

        {form_link}

        Best regards,
        Admin
        """
        from_email = "settings.EMAIL_HOST_USER"
        recipient_list = [recipient_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect("success_page")  # Redirect to success page

    return render(request, "survey_app/form_template.html", {"form": form})




# def send_invite_email(request):
#     if request.method == 'POST':
#         form = FormModelForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             # user.set_password('temp_password')  # Temporary password
#             user.save()
#             link = f"http://127.0.0.1:8000/survey/{user.id}/"
#             send_mail(
#                 'Survey Link',
#                 f'Click this link to fill out the survey: {link}',
#                 'your_email@example.com',
#                 [user.email]
#             )
#             return redirect('survey_sent')
#     else:
#         form = FormModelForm()
#     return render(request, 'survey_app/form_template.html', {'form': form})


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
