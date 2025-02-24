from django.urls import path
from . import views
from .views import submit_expense

urlpatterns = [
    path('send_email/', views.Survey_email, name='send_email'),
    path('fill_form/<str:Unique_id>/', views.submit_expense, name='fill_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve/<int:form_id>/', views.approve, name='approve_form'),
    path('dashboard-user/<int:form_id>/', views.dashboard_user, name='dashboard_user'),
    path("submit_expense/<str:Unique_id>/", submit_expense, name="submit_expense"),
]


