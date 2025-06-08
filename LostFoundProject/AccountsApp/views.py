from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
