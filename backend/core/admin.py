from django.contrib import admin
from .models import Company, Attachment

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_manufacturer', 'is_vendor', 'website')
    search_fields = ('name',)
    list_filter = ('is_manufacturer', 'is_vendor')
    
    fieldsets = (
        ("General", {
            "fields": ("name", "website")
        }),
        ("Roles", {
            "fields": ("is_manufacturer", "is_vendor")
        }),
        ("Contact Info", {
            "fields": ("contacts",)
        }),
        ("Metadata", {
            "fields": ("tags", "custom_fields")
        }),
    )

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file_type', 'size', 'created_at')
    search_fields = ('filename',)
    list_filter = ('file_type',)
