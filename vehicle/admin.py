from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User

from vehicle.models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if not user.is_superuser:
            qs = qs.filter(users=user)
        return qs

    def display_users(self, obj):
        return ', '.join([user.name for user in obj.users.all()])

    display_users.short_description = 'Users'

    list_display = ['id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'display_users', 'createdBy', 'createdDate', 'lastModifiedBy', 'lastModifiedDate']
    list_display_links = ('id',)
    list_filter = ('id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'users',)
    search_fields = ('id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'users')
    readonly_fields = ('createdDate', 'lastModifiedDate')
    list_per_page = 25

    fieldsets = (
        ('General Information', {
            'fields': ('plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'users')
        }),
        ('Timestamps', {
            'fields': ('createdDate', 'lastModifiedDate'),
            'classes': ('collapse',),
        }),
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Users', is_stacked=False)},
    }


admin.site.register(Vehicle, VehicleAdmin)

# from django.contrib import admin
# from django.db import models
#
# from vehicle.models import Vehicle
# from django.contrib.admin.widgets import FilteredSelectMultiple
#
#
# class VehicleAdmin(admin.ModelAdmin):
#     def display_users(self, obj):
#         return ', '.join([user.name for user in obj.users.all()])
#
#     display_users.short_description = 'Users'
#
#     list_display = ['id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'display_users', 'createdBy', 'createdDate', 'lastModifiedBy', 'lastModifiedDate']
#     list_display_links = ('id',)
#     list_filter = ('id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'users__name')
#     search_fields = ('id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'display_users__name')
#     readonly_fields = ('createdDate', 'lastModifiedDate')
#     list_per_page = 25
#
#     fieldsets = (
#         ('General Information', {
#             'fields': ('plates', 'brand', 'colour', 'model', 'serialNumber', 'alive', 'users')
#         }),
#         ('Timestamps', {
#             'fields': ('createdDate', 'lastModifiedDate'),
#             'classes': ('collapse',),
#         }),
#     )
#
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': FilteredSelectMultiple('Users', is_stacked=False)},
#     }
#
#
# admin.site.register(Vehicle, VehicleAdmin)
