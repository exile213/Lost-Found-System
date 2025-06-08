from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def claim_item(request):
    return render(request, 'claims/claim-item.html')
