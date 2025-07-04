from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClaimRequestForm
from .models import ClaimRequest
from ReportsApp.models import ItemReport
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.

@login_required
def claim_item(request, item_id):
    if hasattr(request.user, 'role') and request.user.role == 'staff':
        return render(request, 'claims/claim-item.html', {'error': 'Staff cannot submit claims.'})
    
    try:
        item = ItemReport.objects.get(id=item_id)
        
        # Check if item exists and is available for claiming
        if item.status != 'found':
            return render(request, 'claims/claim-item.html', {
                'error': f'This item is not available for claiming. Current status: {item.status.title()}'
            })
        
        # Check if user is trying to claim their own item
        if item.reporter == request.user:
            return render(request, 'claims/claim-item.html', {
                'error': 'You cannot claim your own reported item.'
            })
        
        # Check if item already has a pending claim from this user
        existing_claim = ClaimRequest.objects.filter(item=item, claimer=request.user, is_verified=False).first()
        if existing_claim:
            return render(request, 'claims/claim-item.html', {
                'error': 'You have already submitted a claim for this item. Please wait for staff review.'
            })
        
        # Check if item already has an approved claim
        approved_claim = ClaimRequest.objects.filter(item=item, is_verified=True).first()
        if approved_claim:
            return render(request, 'claims/claim-item.html', {
                'error': 'This item has already been claimed by another user.'
            })
        
    except ItemReport.DoesNotExist:
        return render(request, 'claims/claim-item.html', {
            'error': 'The requested item could not be found. It may have been removed or the link may be invalid.'
        })
    
    if request.method == 'POST':
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimer = request.user
            claim.save()
            return render(request, 'claims/claim-success.html', {'item': item})
    else:
        form = ClaimRequestForm()
    
    return render(request, 'claims/claim-item.html', {'form': form, 'item': item})

@login_required
def claim_verification(request, claim_id, action):
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access this page.')
    claim = get_object_or_404(ClaimRequest, id=claim_id, is_verified=False)
    if action == 'approve':
        claim.is_verified = True
        claim.verified_by = request.user
        claim.verified_at = timezone.now()
        claim.item.status = 'claimed'
        claim.item.save()
        claim.save()
        messages.success(request, f'Claim for {claim.item.title} has been approved.')
    elif action == 'reject':
        claim.verified_by = request.user
        claim.verified_at = timezone.now()
        claim.save()
        messages.success(request, f'Claim for {claim.item.title} has been rejected.')
    return redirect('accounts:staff_dashboard')

@login_required
def my_claims(request):
    if hasattr(request.user, 'role') and request.user.role == 'staff':
        return HttpResponseForbidden('Staff cannot view personal claims.')
    user_claims = ClaimRequest.objects.filter(claimer=request.user).order_by('-submitted_at')
    return render(request, 'claims/my_claims.html', {'claims': user_claims})

@login_required
def staff_manage_claims(request):
    """Staff view to manage all claims"""
    if not hasattr(request.user, 'role') or request.user.role != 'staff':
        return HttpResponseForbidden('You are not authorized to access this page.')
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    claims = ClaimRequest.objects.all().select_related('item', 'claimer', 'verified_by').order_by('-submitted_at')
    
    # Apply filters
    if status_filter:
        if status_filter == 'pending':
            claims = claims.filter(is_verified=False)
        elif status_filter == 'approved':
            claims = claims.filter(is_verified=True, verified_by__isnull=False)
        elif status_filter == 'rejected':
            claims = claims.filter(is_verified=True, verified_by__isnull=True)
    
    if search_query:
        claims = claims.filter(
            Q(item__title__icontains=search_query) |
            Q(claimer__username__icontains=search_query) |
            Q(claimer__email__icontains=search_query) |
            Q(item__category__name__icontains=search_query) |
            Q(item__location__name__icontains=search_query)
        )
    
    # Get counts for filter tabs
    total_claims = ClaimRequest.objects.count()
    pending_claims = ClaimRequest.objects.filter(is_verified=False).count()
    approved_claims = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=False).count()
    rejected_claims = ClaimRequest.objects.filter(is_verified=True, verified_by__isnull=True).count()
    
    return render(request, 'claims/staff_manage_claims.html', {
        'claims': claims,
        'total_claims': total_claims,
        'pending_claims': pending_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'current_status': status_filter,
        'search_query': search_query,
    })
