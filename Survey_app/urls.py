from django.urls import path
from . import views
from .views import submit_expense_with_id,send_invite_email,submit_expense,fill_form,success_page, approve_form,admin_review_forms,submit_form

urlpatterns = [
    path('submit_expense_with_id/<str:unique_id>/', submit_expense_with_id, name='submit_expense_with_id'),
    path('submit_expense/', submit_expense, name='submit_expense'),
    path("submit/", submit_form, name="submit_form"),
    path('send_email/',send_invite_email, name='send_email'),
    # path('fill_form/<str:unique_id>/',submit_expense_with_id , name='fill_form'),
    path('fill_form/<str:unique_id>/',fill_form , name='fill_form'),
    path("success/",success_page, name="success_page"),
    path("admin/review_forms/", admin_review_forms, name="admin_review_forms"),
    path("admin/approve_form/", approve_form, name="approve_form"),
    
]


