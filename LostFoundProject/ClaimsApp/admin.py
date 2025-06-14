from django.contrib import admin
from .models import ClaimRequest

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimer', 'status', 'submitted_at', 'verified_by', 'verified_at')
    list_filter = ('is_verified', 'submitted_at', 'verified_at', 'item__category', 'item__status')
    search_fields = ('claimer__username', 'claimer__email', 'item__title', 'reason')
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Item Information', {
            'fields': ('item', 'claimer')
        }),
        ('Claim Details', {
            'fields': ('reason', 'additional_proof')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by', 'verified_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )
    
    def status(self, obj):
        if obj.is_verified:
            if obj.verified_by:
                return 'Approved'
            else:
                return 'Rejected'
        return 'Pending'
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('item', 'claimer', 'verified_by')
