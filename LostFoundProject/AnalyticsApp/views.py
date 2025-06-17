from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import get_user_model
from ReportsApp.models import ItemReport, Category, Location
from ClaimsApp.models import ClaimRequest
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, FloatField, IntegerField
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
    date_from = request.GET.get('date_from', '2021-06-01')  # Default to June 2021
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
        base_queryset = base_queryset.filter(category_id=category_filter)
    
    # ==================== DESCRIPTIVE ANALYTICS ====================
    
    # 1. Most commonly lost item categories
    category_analytics = base_queryset.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # 2. Most frequent loss locations
    location_analytics = base_queryset.values('location__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # 3. Lost items reported per month (based on date_lost_or_found)
    monthly_analytics = []
    yearly_analytics = {}  # New dictionary for yearly data
    
    # Get the date range for analytics
    if date_from:
        start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
    else:
        start_date = datetime(2021, 6, 1).date()  # Default to June 2021
    
    end_date = datetime.strptime(date_to, '%Y-%m-%d').date() if date_to else timezone.now().date()
    
    # Generate monthly data points and collect yearly data
    current_date = start_date
    while current_date <= end_date:
        month_start = current_date.replace(day=1)
        if current_date.month == 12:
            month_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
        
        month_reports = base_queryset.filter(
            date_lost_or_found__gte=month_start,
            date_lost_or_found__lte=month_end
        ).count()
        
        # Add to monthly analytics
        monthly_analytics.append({
            'month': month_start.strftime('%B %Y'),
            'count': month_reports,
            'short_month': month_start.strftime('%b %Y')
        })
        
        # Add to yearly analytics
        year = month_start.year
        if year not in yearly_analytics:
            yearly_analytics[year] = {
                'total': 0,
                'months': 0
            }
        yearly_analytics[year]['total'] += month_reports
        yearly_analytics[year]['months'] += 1
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Calculate average monthly reports for each year
    for year_data in yearly_analytics.values():
        year_data['avg_monthly'] = year_data['total'] / year_data['months'] if year_data['months'] > 0 else 0
        del year_data['months']  # Remove the months count as it's no longer needed
    
    yearly_analytics = dict(sorted(yearly_analytics.items()))  # Sort years chronologically
    
    # Prepare data for Chart.js
    chart_data = {
        'categories': {
            'labels': [item['category__name'] for item in category_analytics if item['category__name']],
            'data': [item['count'] for item in category_analytics if item['category__name']]
        },
        'locations': {
            'labels': [item['location__name'] for item in location_analytics if item['location__name']],
            'data': [item['count'] for item in location_analytics if item['location__name']]
        },
        'monthly': {
            'labels': [item['short_month'] for item in monthly_analytics],
            'data': [item['count'] for item in monthly_analytics]
        }
    }
    
    # Get filter options
    all_categories = Category.objects.all().order_by('name')
    
    # Generate insights based on the data
    insights = []
    
    # Insight 1: Most common lost item category
    if category_analytics:
        top_category = category_analytics[0]
        top_percentage = (top_category['count'] / base_queryset.count()) * 100 if base_queryset.count() > 0 else 0
        insights.append({
            'type': 'warning',
            'title': 'Most Common Lost Item',
            'message': f"{top_category['category__name']} items are lost most frequently ({top_category['count']} times, {top_percentage:.1f}% of all reports).",
            'action': 'Focus awareness campaigns and tracking systems on this category',
            'icon': 'alert-triangle',
            'tab': 'categories'
        })
    
    # Insight 2: High-risk location
    if location_analytics:
        riskiest_location = location_analytics[0]
        location_percentage = (riskiest_location['count'] / base_queryset.count()) * 100 if base_queryset.count() > 0 else 0
        if riskiest_location['count'] > 5:  # Only show if significant number of items
            insights.append({
                'type': 'alert',
                'title': 'High-Risk Location',
                'message': f"{riskiest_location['location__name']} has {riskiest_location['count']} lost items ({location_percentage:.1f}% of all reports).",
                'action': 'Implement location-specific awareness and security measures',
                'icon': 'map-pin',
                'tab': 'locations'
            })
    
    # Insight 3: Seasonal trend
    if monthly_analytics:
        max_month = max(monthly_analytics, key=lambda x: x['count'])
        min_month = min(monthly_analytics, key=lambda x: x['count'])
        if max_month['count'] > min_month['count'] * 1.5:  # 50% more activity
            peak_percentage = (max_month['count'] / base_queryset.count()) * 100 if base_queryset.count() > 0 else 0
            insights.append({
                'type': 'info',
                'title': 'Seasonal Pattern Detected',
                'message': f"Peak activity in {max_month['month']} with {max_month['count']} items ({peak_percentage:.1f}%) vs {min_month['count']} in {min_month['month']}.",
                'action': 'Prepare targeted campaigns for high-risk periods',
                'icon': 'trending-up',
                'tab': 'monthly'
            })
    
    # Insight 4: Overall statistics insight
    total_reports = base_queryset.count()
    total_lost = base_queryset.filter(status='lost').count()
    total_found = base_queryset.filter(status='found').count()
    total_claimed = base_queryset.filter(status='claimed').count()
    if total_lost > total_found:
        lost_percentage = (total_lost / total_reports) * 100 if total_reports > 0 else 0
        insights.append({
            'type': 'warning',
            'title': 'Lost vs Found Imbalance',
            'message': f"More items are being lost ({total_lost}, {lost_percentage:.1f}%) than found ({total_found}).",
            'action': 'Strengthen recovery and awareness programs',
            'icon': 'scale'
        })
    else:
        found_percentage = (total_found / total_reports) * 100 if total_reports > 0 else 0
        insights.append({
            'type': 'success',
            'title': 'Good Recovery Rate',
            'message': f"More items are being found ({total_found}, {found_percentage:.1f}%) than lost ({total_lost}).",
            'action': 'Maintain current recovery efforts',
            'icon': 'check-circle'
        })
    
    # Insight 5: Category diversity
    if len(category_analytics) > 5:
        insights.append({
            'type': 'info',
            'title': 'High Category Diversity',
            'message': f"Items are lost across {len(category_analytics)} different categories, indicating diverse campus activities.",
            'action': 'Implement broad awareness campaigns covering multiple categories',
            'icon': 'layers'
        })
    
    # Insight 6: Location concentration
    if location_analytics and len(location_analytics) <= 3:
        insights.append({
            'type': 'warning',
            'title': 'Location Concentration',
            'message': f"Lost items are concentrated in only {len(location_analytics)} locations, suggesting specific problem areas.",
            'action': 'Focus resources on these high-risk locations',
            'icon': 'target'
        })

    context = {
        # Descriptive Analytics
        'category_analytics': category_analytics,
        'location_analytics': location_analytics,
        'monthly_analytics': monthly_analytics,
        'yearly_analytics': yearly_analytics,  # Add yearly analytics to context
        
        # Chart Data
        'chart_data': json.dumps(chart_data),
        
        # Summary statistics
        'total_reports': total_reports,
        'total_lost': total_lost,
        'total_found': total_found,
        'total_claimed': total_claimed,
        
        # Filter options
        'all_categories': all_categories,
        'date_from': date_from,
        'date_to': date_to,
        'category_filter': category_filter,
        'insights': insights,
    }
    
    return render(request, 'analytics/descriptive.html', context)

@login_required
def diagnostic_analytics_view(request):
    """Diagnostic Analytics: Claim Success, Active Reporters, Low Claim Items"""
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get the User model
    User = get_user_model()
    
    # Get filter parameters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
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
    
    # ==================== DIAGNOSTIC ANALYTICS ====================
    
    # 1. Items that are frequently reported but rarely claimed
    item_claim_analytics = []
    items_with_claims = base_queryset.annotate(
        total_claims=Count('claimrequest'),
        successful_claims=Count('claimrequest', filter=Q(claimrequest__is_verified=True))
    ).filter(total_claims__gt=0)
    
    for item in items_with_claims[:10]:  # Top 10 items
        success_rate = (item.successful_claims / item.total_claims) * 100 if item.total_claims > 0 else 0
        item_claim_analytics.append({
            'item': item,
            'total_claims': item.total_claims,
            'successful_claims': item.successful_claims,
            'success_rate': round(success_rate, 1)
        })
    
    # 2. Most active reporters (users who report the most items)
    active_reporters = base_queryset.values(
        'reporter__username',
        'reporter__first_name',
        'reporter__last_name'
    ).annotate(
        report_count=Count('id')
    ).order_by('-report_count')[:10]
    
    # Prepare chart data
    chart_data = {
        'active_reporters': {
            'labels': [reporter['reporter__username'] for reporter in active_reporters],
            'data': [reporter['report_count'] for reporter in active_reporters]
        }
    }
    
    # Calculate total reports for insights
    total_reports = base_queryset.count()
    
    # Generate insights based on the data
    insights = []
    
    # Insight 1: Most frequent reporter
    if active_reporters:
        top_reporter = active_reporters[0]
        if top_reporter['report_count'] >= 3:
            reporter_percentage = (top_reporter['report_count'] / total_reports) * 100 if total_reports > 0 else 0
            insights.append({
                'type': 'warning',
                'title': 'Frequent Reporter',
                'message': f"{top_reporter['reporter__username']} has reported {top_reporter['report_count']} items ({reporter_percentage:.1f}% of all reports).",
                'action': 'Consider providing organizational support or training',
                'icon': 'user',
                'tab': 'reporters'
            })
    
    # Insight 2: Reporter behavior patterns
    if len(active_reporters) >= 3:
        insights.append({
            'type': 'info',
            'title': 'Multiple Frequent Reporters',
            'message': f"Found {len(active_reporters)} users with multiple reports, indicating potential patterns in campus behavior.",
            'action': 'Analyze common factors among frequent reporters',
            'icon': 'users'
        })

    context = {
        # Diagnostic Analytics
        'item_claim_analytics': item_claim_analytics,
        'active_reporters': active_reporters,
        
        # Chart Data
        'chart_data': json.dumps(chart_data),
        
        # Summary statistics
        'total_reports': total_reports,
        'total_claims': ClaimRequest.objects.count(),
        'successful_claims': ClaimRequest.objects.filter(is_verified=True).count(),
        
        # Filter options
        'date_from': date_from,
        'date_to': date_to,
        'insights': insights,
    }
    
    return render(request, 'analytics/diagnostic.html', context)

@login_required
def search(request):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    status = request.GET.get('status', '')
    date_filter = request.GET.get('date_filter', '')
    
    # Start with all items
    items = ItemReport.objects.all().order_by('-timestamp_reported')
    
    # Apply filters
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(reporter__username__icontains=search_query)
        )
    
    if category_id:
        items = items.filter(category_id=category_id)
    
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
    categories = Category.objects.all().order_by('name')
    
    # Get counts for each status
    total_items = items.count()
    lost_count = items.filter(status='lost').count()
    found_count = items.filter(status='found').count()
    claimed_count = items.filter(status='claimed').count()
    
    context = {
        'items': items,
        'search_query': search_query,
        'category': category_id,
        'status': status,
        'date_filter': date_filter,
        'categories': categories,
        'total_items': total_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
    }
    
    return render(request, 'analytics/search.html', context)
