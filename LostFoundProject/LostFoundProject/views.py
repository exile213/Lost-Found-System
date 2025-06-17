from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ReportsApp.models import ItemReport, Category, Location
from ClaimsApp.models import ClaimRequest
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    user = request.user
    
    # Get user's reports
    user_lost_items = ItemReport.objects.filter(reporter=user, status='lost').count()
    user_found_items = ItemReport.objects.filter(reporter=user, status='found').count()
    
    # Get pending claims (claims made by user that are not verified)
    pending_claims = ClaimRequest.objects.filter(claimer=user, is_verified=False).count()
    
    # Get recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_reports = ItemReport.objects.filter(
        reporter=user,
        timestamp_reported__gte=seven_days_ago
    ).order_by('-timestamp_reported')[:5]
    
    # Get recent claims
    recent_claims = ClaimRequest.objects.filter(
        claimer=user,
        submitted_at__gte=seven_days_ago
    ).order_by('-submitted_at')[:5]
    
    # Get items that match user's lost reports (potential matches)
    user_lost_reports = ItemReport.objects.filter(reporter=user, status='lost')
    potential_matches = []
    
    for lost_report in user_lost_reports:
        # Find found items with similar category and location
        similar_found_items = ItemReport.objects.filter(
            status='found',
            category=lost_report.category,
            timestamp_reported__gte=lost_report.timestamp_reported
        ).exclude(reporter=user)[:3]
        potential_matches.extend(similar_found_items)
    
    # Remove duplicates and limit to 5
    potential_matches = list(set(potential_matches))[:5]
    
    context = {
        'user_lost_items': user_lost_items,
        'user_found_items': user_found_items,
        'pending_claims': pending_claims,
        'recent_reports': recent_reports,
        'recent_claims': recent_claims,
        'potential_matches': potential_matches,
        'has_activity': bool(recent_reports or recent_claims or potential_matches),
    }
    
    return render(request, 'dashboard.html', context)

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def report_lost(request):
    return render(request, 'reports/report-lost.html')

def report_found(request):
    return render(request, 'reports/report-found.html')

def search(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    location_id = request.GET.get('location', '')
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
            Q(category__name__icontains=search_query)
        )
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    if location_id:
        items = items.filter(location_id=location_id)
    
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
    
    # Get unique categories and locations for filter dropdowns
    categories = Category.objects.all().order_by('name')
    locations = Location.objects.all().order_by('name')
    
    # Get counts for each status (before pagination)
    total_items = items.count()
    lost_count = items.filter(status='lost').count()
    found_count = items.filter(status='found').count()
    claimed_count = items.filter(status='claimed').count()
    
    # Pagination
    paginator = Paginator(items, 12)  # Show 12 items per page
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        items = paginator.page(paginator.num_pages)
    
    context = {
        'items': items,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_location': location_id,
        'selected_status': status,
        'selected_date_filter': date_filter,
        'categories': categories,
        'locations': locations,
        'total_items': total_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
    }
    
    return render(request, 'search.html', context)

def my_reports(request):
    return render(request, 'reports/my-reports.html')

def claim_item(request):
    return render(request, 'claim-item.html')

def user_guide(request):
    return render(request, 'user-guide.html')