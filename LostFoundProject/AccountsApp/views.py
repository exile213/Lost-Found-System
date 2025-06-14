from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from ReportsApp.models import ItemReport
from ClaimsApp.models import ClaimRequest
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'accounts/login.html', {'email': email})
        User = get_user_model()
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
            return render(request, 'accounts/login.html', {'email': email})
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                if hasattr(user, 'role') and user.role == 'staff':
                    return redirect('accounts:staff_dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
        return render(request, 'accounts/login.html', {'email': email})
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'upload_photo':
            if 'profile_picture' in request.FILES:
                user = request.user
                user.profile_picture = request.FILES['profile_picture']
                user.save()
                messages.success(request, 'Profile picture updated successfully!')
            else:
                messages.error(request, 'Please select a file to upload.')
            return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')

def register(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        role = request.POST.get('role')

        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            student_id=student_id,
            department=department,
            role=role
        )
        user.is_active = True
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('accounts:login')
    return render(request, 'accounts/register.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.student_id = request.POST.get('student_id', '')
        user.department = request.POST.get('department', '')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'accounts/staff_login.html', {'email': email})
        
        User = get_user_model()
        
        # First, check if user exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
            return render(request, 'accounts/staff_login.html', {'email': email})
        
        # Check if user is active
        if not user_obj.is_active:
            messages.error(request, 'Your account is inactive. Please contact support.')
            return render(request, 'accounts/staff_login.html', {'email': email})
        
        # Check if user has staff role (our custom field, not Django's is_staff)
        if not hasattr(user_obj, 'role') or user_obj.role != 'staff':
            messages.error(request, f'You are not authorized to log in as staff. Your current role is: {getattr(user_obj, "role", "None")}')
            return render(request, 'accounts/staff_login.html', {'email': email})
        
        # Now authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Double-check that the authenticated user has staff role
            if hasattr(user, 'role') and user.role == 'staff':
                auth_login(request, user)
                messages.success(request, 'Staff login successful!')
                return redirect('accounts:staff_dashboard')
            else:
                messages.error(request, 'Authentication successful but you do not have staff privileges.')
                return render(request, 'accounts/staff_login.html', {'email': email})
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return render(request, 'accounts/staff_login.html', {'email': email})
    
    return render(request, 'accounts/staff_login.html')

@login_required
def staff_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access this page.')
    
    # Get the User model
    User = get_user_model()
    
    # Get pending claims
    pending_claims = ClaimRequest.objects.filter(is_verified=False)
    
    # Get additional stats
    approved_claims_count = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=False).count()
    rejected_claims_count = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=True).count()
    total_users_count = User.objects.count()
    
    return render(request, 'accounts/staff_dashboard.html', {
        'pending_claims': pending_claims,
        'approved_claims_count': approved_claims_count,
        'rejected_claims_count': rejected_claims_count,
        'total_users_count': total_users_count,
        'show_analytics': True,
    })

@login_required
def staff_reports(request):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access this page.')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    date_filter = request.GET.get('date_filter', '')
    
    # Start with all reports
    reports = ItemReport.objects.all().order_by('-timestamp_reported')
    
    # Apply filters
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(reporter__username__icontains=search_query)
        )
    
    if category:
        reports = reports.filter(category=category)
    
    if status:
        reports = reports.filter(status=status)
    
    # Apply date filters
    if date_filter:
        today = timezone.now().date()
        if date_filter == 'today':
            reports = reports.filter(date_lost_or_found=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            reports = reports.filter(date_lost_or_found__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            reports = reports.filter(date_lost_or_found__gte=month_ago)
    
    # Get unique categories for filter dropdown
    categories = ItemReport.objects.values_list('category', flat=True).distinct()
    
    # Get counts for each status
    total_reports = reports.count()
    lost_count = reports.filter(status='lost').count()
    found_count = reports.filter(status='found').count()
    claimed_count = reports.filter(status='claimed').count()
    
    context = {
        'reports': reports,
        'search_query': search_query,
        'category': category,
        'status': status,
        'date_filter': date_filter,
        'categories': categories,
        'total_reports': total_reports,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
    }
    
    return render(request, 'accounts/staff_reports.html', context)
