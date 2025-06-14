from django.contrib import admin
from .models import ItemReport

@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'reporter', 'date_lost_or_found', 'timestamp_reported')
    list_filter = ('status', 'category', 'date_lost_or_found', 'timestamp_reported')
    search_fields = ('title', 'description', 'location', 'reporter__username', 'reporter__email')
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
        return super().get_queryset(request).select_related('reporter')
