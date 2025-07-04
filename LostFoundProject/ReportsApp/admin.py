from django.contrib import admin
from .models import ItemReport, Category, Location

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'reporter', 'date_lost_or_found', 'timestamp_reported')
    list_filter = ('status', 'category', 'location', 'date_lost_or_found', 'timestamp_reported')
    search_fields = ('title', 'description', 'location__name', 'category__name', 'reporter__username', 'reporter__email')
    readonly_fields = ('timestamp_reported',)
    date_hierarchy = 'timestamp_reported'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Location & Date', {
            'fields': ('location', 'date_lost_or_found', 'time_lost_or_found')
        }),
        ('Status & Reporter', {
            'fields': ('status', 'reporter')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('timestamp_reported',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reporter', 'category', 'location') 