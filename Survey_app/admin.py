from django.contrib import admin
from .models import Form

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('Email', 'Created_Time', 'approve')
    list_filter = ('approve',)
    actions = ['approve_responses']

    def approve_responses(self, request, queryset):
        queryset.update(approve=True)
    approve_responses.short_description = "Approve selected responses"


