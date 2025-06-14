from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import get_user_model
from ReportsApp.models import ItemReport
from ClaimsApp.models import ClaimRequest
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from datetime import timedelta, datetime
import json
from collections import defaultdict

# Create your views here.

@login_required
def analytics_home_redirect(request):
    """Redirect to descriptive analytics as the default analytics page"""
    return redirect('analytics:descriptive')

@login_required
def descriptive_analytics_view(request):
    """Descriptive Analytics: Categories, Locations, Monthly Trends"""
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get the User model
    User = get_user_model()
    
    # Get filter parameters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    category_filter = request.GET.get('category', '')
    
    # Base queryset with filters
    base_queryset = ItemReport.objects.all()
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            base_queryset = base_queryset.filter(date_lost_or_found__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            base_queryset = base_queryset.filter(date_lost_or_found__lte=date_to_obj)
        except ValueError:
            pass
    
    if category_filter:
        base_queryset = base_queryset.filter(category=category_filter)
    
    # ==================== DESCRIPTIVE ANALYTICS ====================
    
    # 1. Most commonly lost item categories
    category_analytics = base_queryset.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # 2. Most frequent loss locations
    location_analytics = base_queryset.values('location').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # 3. Lost items reported per month (last 12 months)
    monthly_analytics = []
    for i in range(12):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_reports = base_queryset.filter(
            timestamp_reported__gte=month_start,
            timestamp_reported__lte=month_end
        ).count()
        
        monthly_analytics.append({
            'month': month_start.strftime('%B %Y'),
            'count': month_reports,
            'short_month': month_start.strftime('%b %Y')
        })
    
    monthly_analytics.reverse()  # Show oldest to newest
    
    # Prepare data for Chart.js
    chart_data = {
        'categories': {
            'labels': [item['category'].title() for item in category_analytics],
            'data': [item['count'] for item in category_analytics]
        },
        'locations': {
            'labels': [item['location'] for item in location_analytics],
            'data': [item['count'] for item in location_analytics]
        },
        'monthly': {
            'labels': [item['short_month'] for item in monthly_analytics],
            'data': [item['count'] for item in monthly_analytics]
        }
    }
    
    # Get filter options
    all_categories = ItemReport.objects.values_list('category', flat=True).distinct()
    
    context = {
        # Descriptive Analytics
        'category_analytics': category_analytics,
        'location_analytics': location_analytics,
        'monthly_analytics': monthly_analytics,
        
        # Chart Data
        'chart_data': json.dumps(chart_data),
        
        # Summary statistics
        'total_reports': base_queryset.count(),
        
        # Filter options
        'all_categories': all_categories,
        'date_from': date_from,
        'date_to': date_to,
        'category_filter': category_filter,
    }
    
    return render(request, 'analytics/descriptive.html', context)

@login_required
def diagnostic_analytics_view(request):
    """Diagnostic Analytics: Departments, Claim Success, Active Reporters, Low Claim Items"""
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get the User model
    User = get_user_model()
    
    # Get filter parameters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    department_filter = request.GET.get('department', '')
    
    # Base queryset with filters
    base_queryset = ItemReport.objects.all()
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            base_queryset = base_queryset.filter(date_lost_or_found__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            base_queryset = base_queryset.filter(date_lost_or_found__lte=date_to_obj)
        except ValueError:
            pass
    
    if department_filter:
        base_queryset = base_queryset.filter(reporter__department=department_filter)
    
    # ==================== DIAGNOSTIC ANALYTICS ====================
    
    # 1. Departments with highest item loss counts
    department_analytics = base_queryset.values(
        'reporter__department'
    ).annotate(
        count=Count('id')
    ).filter(
        reporter__department__isnull=False
    ).exclude(
        reporter__department=''
    ).order_by('-count')[:10]
    
    # 2. Items that are frequently reported but rarely claimed
    item_claim_analytics = []
    items_with_claims = base_queryset.annotate(
        total_claims=Count('claimrequest'),
        successful_claims=Count('claimrequest', filter=Q(claimrequest__is_verified=True))
    ).filter(total_claims__gt=0)
    
    for item in items_with_claims:
        if item.total_claims > 0:
            claim_rate = (item.successful_claims / item.total_claims) * 100
            item_claim_analytics.append({
                'item_title': item.title,
                'category': item.category,
                'total_claims': item.total_claims,
                'successful_claims': item.successful_claims,
                'claim_rate': round(claim_rate, 1)
            })
    
    # Sort by claim rate (lowest first) and take top 10
    item_claim_analytics.sort(key=lambda x: x['claim_rate'])
    item_claim_analytics = item_claim_analytics[:10]
    
    # 3. Most active item reporters
    active_reporters = base_queryset.values(
        'reporter__username',
        'reporter__department'
    ).annotate(
        report_count=Count('id')
    ).order_by('-report_count')[:10]
    
    # 4. Success rate by category
    category_success_rates = []
    for category in base_queryset.values_list('category', flat=True).distinct():
        category_items = base_queryset.filter(category=category)
        total_items = category_items.count()
        claimed_items = category_items.filter(status='claimed').count()
        
        if total_items > 0:
            success_rate = (claimed_items / total_items) * 100
            category_success_rates.append({
                'category': category,
                'total_items': total_items,
                'claimed_items': claimed_items,
                'success_rate': round(success_rate, 1)
            })
    
    category_success_rates.sort(key=lambda x: x['success_rate'], reverse=True)
    
    # Prepare data for Chart.js
    chart_data = {
        'departments': {
            'labels': [item['reporter__department'] for item in department_analytics],
            'data': [item['count'] for item in department_analytics]
        },
        'category_success': {
            'labels': [item['category'].title() for item in category_success_rates],
            'data': [item['success_rate'] for item in category_success_rates]
        }
    }
    
    # Get filter options
    all_departments = User.objects.values_list('department', flat=True).filter(
        department__isnull=False
    ).exclude(department='').distinct()
    
    context = {
        # Diagnostic Analytics
        'department_analytics': department_analytics,
        'item_claim_analytics': item_claim_analytics,
        'active_reporters': active_reporters,
        'category_success_rates': category_success_rates,
        
        # Chart Data
        'chart_data': json.dumps(chart_data),
        
        # Summary statistics
        'total_reports': base_queryset.count(),
        'total_claims': ClaimRequest.objects.count(),
        'successful_claims': ClaimRequest.objects.filter(is_verified=True).count(),
        'pending_claims': ClaimRequest.objects.filter(is_verified=False).count(),
        
        # Filter options
        'all_departments': all_departments,
        'date_from': date_from,
        'date_to': date_to,
        'department_filter': department_filter,
    }
    
    return render(request, 'analytics/diagnostic.html', context)

@login_required
def search(request):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    date_filter = request.GET.get('date_filter', '')
    
    # Start with all items
    items = ItemReport.objects.all().order_by('-timestamp_reported')
    
    # Apply filters
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(reporter__username__icontains=search_query)
        )
    
    if category:
        items = items.filter(category=category)
    
    if status:
        items = items.filter(status=status)
    
    # Apply date filters
    if date_filter:
        today = timezone.now().date()
        if date_filter == 'today':
            items = items.filter(date_lost_or_found=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            items = items.filter(date_lost_or_found__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            items = items.filter(date_lost_or_found__gte=month_ago)
    
    # Get unique categories for filter dropdown
    categories = ItemReport.objects.values_list('category', flat=True).distinct()
    
    # Get counts for each status
    total_items = items.count()
    lost_count = items.filter(status='lost').count()
    found_count = items.filter(status='found').count()
    claimed_count = items.filter(status='claimed').count()
    
    context = {
        'items': items,
        'search_query': search_query,
        'category': category,
        'status': status,
        'date_filter': date_filter,
        'categories': categories,
        'total_items': total_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
    }
    
    return render(request, 'analytics/search.html', context)
