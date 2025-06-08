from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('claim-item/', views.claim_item, name='claim_item'),
] 