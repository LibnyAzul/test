from django.contrib import admin

from tracking.models import Tracking


class TrackingAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'latitude', 'longitude', 'createdDate']
    list_filter = ('vehicle',)
    search_fields = ('vehicle__plates',)
    readonly_fields = ('createdDate',)
    fieldsets = (
        ('Tracking Information', {'fields': ('vehicle', 'latitude', 'longitude')}),
        ('Timestamps', {'fields': ('createdDate',), 'classes': ('collapse',)}),
    )


admin.site.register(Tracking, TrackingAdmin)
