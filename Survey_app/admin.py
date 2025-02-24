from django.contrib import admin
from django.contrib import messages
from .models import Form
import random
import string


class AdminForm(admin.ModelAdmin):
    list_display=("Email","Created_Time","approve",)
    list_filter=("approve","Created_Time",)
    search_fields=("Email",)
    actions=["bulk_approve"]

def bulk_approve(self,request,queryset):
        for form in queryset:
            if not form.approve:
                form.Password=''.join(random.choices(string.ascii_letters + string.digits,k=8))
                form.approve=True
                form.save()
        self.message_user(request,"Multiple forms approved successfully",level=messages.SUCCESS)

bulk_approve.short_description="Approve multiple forms"


try:
    admin.site.register(Form,AdminForm)
except admin.sites.AlreadyRegistered:
    pass


