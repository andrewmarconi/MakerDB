from django.contrib import admin
from .models import Project, BOMItem
from parts.models import Part
from core.models import Attachment

class PartInline(admin.TabularInline):
    # Determine which FK links Part to Project
    model = Part
    fk_name = "project"  # Explicitly state the FK field name
    fields = ('name', 'part_type', 'mpn', 'total_stock')
    readonly_fields = ('total_stock',)
    extra = 0
    show_change_link = True

class BOMItemInline(admin.TabularInline):
    model = BOMItem
    extra = 1
    autocomplete_fields = ['part', 'substitutes']
    fields = ('part', 'quantity', 'designators', 'substitutes')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "revision", "status", "created_at")
    search_fields = ("name", "description")
    list_filter = ("status", "created_at")
    inlines = [BOMItemInline] 
    
    fieldsets = (
        ("General", {
            "fields": ("name", "revision", "status", "description", "notes")
        }),
        ("Metadata", {
            "fields": ("tags", "custom_fields")
        }),
    )
