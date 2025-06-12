from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import LostItemReportForm, FoundItemReportForm
from .models import ItemReport

@login_required
def report_lost(request):
    if request.method == 'POST':
        form = LostItemReportForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.status = 'lost'
            item.reporter = request.user
            item.save()
            messages.success(request, f'Lost item "{item.title}" has been successfully reported! We will help you find it.')
            return redirect(f"{reverse('reports:report_lost')}?success=true&message=Lost item '{item.title}' has been successfully reported!")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LostItemReportForm()
    return render(request, 'reports/report-lost.html', {'form': form})

@login_required
def report_found(request):
    if request.method == 'POST':
        form = FoundItemReportForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.status = 'found'
            item.reporter = request.user
            item.save()
            messages.success(request, f'Found item "{item.title}" has been successfully reported! We will help return it to its owner.')
            return redirect(f"{reverse('reports:report_found')}?success=true&message=Found item '{item.title}' has been successfully reported!")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FoundItemReportForm()
    return render(request, 'reports/report-found.html', {'form': form})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(ItemReport, id=report_id, reporter=request.user)
    return render(request, 'reports/report-detail.html', {'report': report})

@login_required
def my_reports(request):
    all_reports = ItemReport.objects.filter(reporter=request.user).order_by('-timestamp_reported')
    
    lost_reports = all_reports.filter(status='lost')
    found_reports = all_reports.filter(status='found')
    
    context = {
        'reports': all_reports,
        'lost_reports': lost_reports,
        'found_reports': found_reports,
        'lost_count': lost_reports.count(),
        'found_count': found_reports.count(),
    }
    
    return render(request, 'reports/my-reports.html', context)
