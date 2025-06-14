from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_home_redirect, name='home'),
    path('dashboard/', views.analytics_home_redirect, name='dashboard'),
    path('descriptive/', views.descriptive_analytics_view, name='descriptive'),
    path('diagnostic/', views.diagnostic_analytics_view, name='diagnostic'),
    path('search/', views.search, name='search'),
] 