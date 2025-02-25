from django.urls import path
from . import views
from .views import submit_expense_with_id,send_invite_email,submit_expense,fill_form,success_page

urlpatterns = [
    path('submit_expense_with_id/<str:Unique_id>/', submit_expense_with_id, name='submit_expense_with_id'),
    path('submit_expense/', submit_expense, name='submit_expense'),
    path('send_email/', send_invite_email, name='send_email'),
    path('fill_form/<str:unique_id>/',submit_expense_with_id , name='fill_form'),
    path('fill_form/<str:unique_id>/',fill_form , name='fill_form'),
    path("success/", success_page, name="success_page"),
    
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('approve/<int:form_id>/', views.approve, name='approve_form'),
    # path('dashboard-user/<int:form_id>/', views.dashboard_user, name='dashboard_user'),
    # path("submit_expense/",views.submit_expense, name="submit_expense"),
]


