from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('claim-item/<int:item_id>/', views.claim_item, name='claim_item'),
    path('claim-verification/<int:claim_id>/<str:action>/', views.claim_verification, name='claim_verification'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('staff/manage/', views.staff_manage_claims, name='staff_manage_claims'),
] 