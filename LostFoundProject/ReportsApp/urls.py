from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('report-lost/', views.report_lost, name='report_lost'),
    path('report-found/', views.report_found, name='report_found'),
    path('my-reports/', views.my_reports, name='my_reports'),
] 