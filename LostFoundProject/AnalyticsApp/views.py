from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from ReportsApp.models import ItemReport
from ClaimsApp.models import ClaimRequest
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@login_required
def dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access analytics. Staff access only.')
    
    # Get the User model
    User = get_user_model()
    
    # Basic statistics
    total_reports = ItemReport.objects.count()
    total_users = User.objects.count()
    total_claims = ClaimRequest.objects.count()
    
    # Status breakdowns
    lost_items = ItemReport.objects.filter(status='lost').count()
    found_items = ItemReport.objects.filter(status='found').count()
    claimed_items = ItemReport.objects.filter(status='claimed').count()
    
    # Claims breakdown
    pending_claims = ClaimRequest.objects.filter(is_verified=False).count()
    approved_claims = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=False).count()
    rejected_claims = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=True).count()
    
    # Category breakdown
    category_stats = ItemReport.objects.values('category').annotate(count=Count('id')).order_by('-count')
    
    # Recent activity (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_reports = ItemReport.objects.filter(timestamp_reported__gte=thirty_days_ago).count()
    recent_claims = ClaimRequest.objects.filter(submitted_at__gte=thirty_days_ago).count()
    
    # Monthly trends (last 6 months)
    monthly_data = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_reports = ItemReport.objects.filter(
            timestamp_reported__gte=month_start,
            timestamp_reported__lte=month_end
        ).count()
        
        month_claims = ClaimRequest.objects.filter(
            submitted_at__gte=month_start,
            submitted_at__lte=month_end
        ).count()
        
        monthly_data.append({
            'month': month_start.strftime('%B %Y'),
            'reports': month_reports,
            'claims': month_claims
        })
    
    # Top locations
    top_locations = ItemReport.objects.values('location').annotate(count=Count('id')).order_by('-count')[:5]
    
    # Staff activity
    staff_verifications = ClaimRequest.objects.filter(verified_by__isnull=False).count()
    
    context = {
        'total_reports': total_reports,
        'total_users': total_users,
        'total_claims': total_claims,
        'lost_items': lost_items,
        'found_items': found_items,
        'claimed_items': claimed_items,
        'pending_claims': pending_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'category_stats': category_stats,
        'recent_reports': recent_reports,
        'recent_claims': recent_claims,
        'monthly_data': monthly_data,
        'top_locations': top_locations,
        'staff_verifications': staff_verifications,
    }
    
    return render(request, 'analytics/dashboard.html', context)

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
