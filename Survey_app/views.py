from django.shortcuts import render,redirect,get_object_or_404
from .models import Form
from django.core.mail import send_mail
from django.conf import settings
import uuid

def Survey_email(request):
    if request.method=='POST':
        Email=request.POST["Email"]
        Unique_id=str(uuid.uuid4())
        Link=f"http://127.0.0.1:8000/Survey/{Unique_id}"

        # save to db
        Form.objects.create(Email=Email,Link=Link)

        # send the email to the user
        send_mail(
            "Survey Form",
            f"Hello,Please fill out this form : {Link}",
            settings.EMAIL_ADMIN_USER,
            [Email],
            fail_silently=True,
        )
        return redirect("Success Page")
    return render(request,Survey_app/send_mail.html)

def fill_form(request,Unique_id):
    form = get_object_or_404(Form, Link=f"http://127.0.0.1:8000/Survey/{Unique_id}/")
    if request.method=="POST":
        tea=request.POST.get("tea",0)
        coffee=request.POST.get("coffee",0)
        smoking=request.POST.get("smoking",0)
        biscuit=request.POST.get("biscuit",0)

        Form.objects.create(
            
        )


        
