from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from user.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'fullName', 'email', 'cellPhone', 'birthdate', 'is_staff', 'alive', 'createdBy', 'createdDate', 'lastModifiedBy', 'lastModifiedDate']
    list_filter = ('is_staff', 'alive')
    search_fields = ('name', 'fullName', 'email')
    ordering = ('-createdDate',)
    readonly_fields = ('createdDate', 'lastModifiedDate')
    fieldsets = (
        ('User Information', {'fields': ('name', 'fullName', 'email', 'cellPhone', 'birthdate', 'is_staff', 'alive')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'fullName', 'email', 'cellPhone', 'birthdate', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
