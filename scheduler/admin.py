from django.contrib import admin
from .models import Prisoner, ActivityType, RequestTemplate, ApprovalProcess, DepartmentRole

# Prisoner Admin
@admin.register(Prisoner)
class PrisonerAdmin(admin.ModelAdmin):
    list_display = ('prisoner_id', 'full_name', 'approved', 'previous_available_date', 'next_available_date')
    search_fields = ('prisoner_id', 'full_name')
    list_filter = ('approved',)
    readonly_fields = ('previous_available_date', 'next_available_date')

# ActivityType Admin
@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# RequestTemplate Admin
@admin.register(RequestTemplate)
class RequestTemplateAdmin(admin.ModelAdmin):
    list_display = ('prisoner', 'activity_type', 'subject', 'status', 'created_at', 'updated_at', 'desired_date')
    search_fields = ('prisoner__full_name', 'activity_type__name', 'subject')
    list_filter = ('status', 'activity_type')
    readonly_fields = ('created_at', 'updated_at', 'date_of_request')
    fieldsets = (
        (None, {
            'fields': ('prisoner', 'activity_type', 'subject', 'details', 'desired_date', 'status', 'created_by')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'contact_name', 'contact_relationship')
        }),
        ('Confirmation', {
            'fields': ('image_confirmation',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'date_of_request')
        }),
    )

# ApprovalProcess Admin
@admin.register(ApprovalProcess)
class ApprovalProcessAdmin(admin.ModelAdmin):
    list_display = ('request_template', 'approved_by', 'status', 'approved_at')
    search_fields = ('request_template__subject', 'approved_by__username')
    list_filter = ('status',)
    readonly_fields = ('approved_at',)

# DepartmentRole Admin
@admin.register(DepartmentRole)
class DepartmentRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    ordering = ('order',)
