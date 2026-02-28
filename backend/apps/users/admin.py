from django.contrib import admin
from .models import User, UserRole
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# Register your models here.

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1
    fk_name = 'user'
    fields = ('role', 'is_active', 'expires_at', 'granted_by', 'granted_at')
    readonly_fields = ('granted_at',)
    autocomplete_fields = ('granted_by',)

@admin.register(User)
class BaseUserAdmin(DjangoUserAdmin):
    inlines = [UserRoleInline]

    # What you see in the list view
    list_display  = ('email', 'auth_provider', 'is_active', 'is_staff', 'date_joined')
    list_filter   = ('is_active', 'is_staff', 'auth_provider')
    search_fields = ('email',)
    ordering      = ('-date_joined',)

    # The edit/detail view — replaces DjangoUserAdmin.fieldsets
    # which references 'username' and would crash
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Metadata', {
            'fields': ('auth_provider',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),  # hidden by default, reduces clutter
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # The create view — DjangoUserAdmin.add_fieldsets also references 'username'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # These are read-only on the detail view
    readonly_fields = ('date_joined', 'last_login')

