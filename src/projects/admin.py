from django.contrib import admin
from .models import Project
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

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
    inlines = [PartInline]
