from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('report-lost/', views.report_lost, name='report_lost'),
    path('report-found/', views.report_found, name='report_found'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('item/<int:report_id>/', views.item_detail, name='item_detail'),
] 