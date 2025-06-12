from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def report_lost(request):
    return render(request, 'reports/report-lost.html')

def report_found(request):
    return render(request, 'reports/report-found.html')

def search(request):
    return render(request, 'search.html')

def my_reports(request):
    return render(request, 'reports/my-reports.html')

def claim_item(request):
    return render(request, 'claim-item.html')

def user_guide(request):
    return render(request, 'user-guide.html')