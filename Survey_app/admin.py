from django.contrib import admin
from .models import Form

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('Email', 'Created_Time', 'isapprove')
    list_filter = ('isapprove',)
    actions = ['approve_responses']

    def approve_responses(self, request, queryset):
        queryset.update(isapprove=True)
        self.message_user(request, "Selected forms have been approved.")
    approve_responses.short_description = "Approve selected responses"


