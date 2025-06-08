from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def report_lost(request):
    return render(request, 'reports/report-lost.html')

@login_required
def report_found(request):
    return render(request, 'reports/report-found.html')

@login_required
def my_reports(request):
    return render(request, 'reports/my-reports.html')
