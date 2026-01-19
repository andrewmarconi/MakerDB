from django.contrib import admin
from .models import Part
from inventory.models import Stock
from procurement.models import Offer

class StockInline(admin.TabularInline):
    model = Stock
    extra = 0
    fields = ('storage', 'quantity', 'status', 'lot', 'updated_at')
    readonly_fields = ('updated_at',)
    show_change_link = True

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0
    fields = ('vendor', 'sku', 'moq', 'prices', 'offer_type')
    show_change_link = True

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'mpn', 'part_type', 'total_stock', 'manufacturer')
    search_fields = ('name', 'mpn', 'description')
    list_filter = ('part_type', 'manufacturer')
    
    # Inline configuration to augment the tabbed view
    inlines = [StockInline, OfferInline]

    fieldsets = (
        ("General", {
            "fields": ("name", "part_type", "description", "notes")
        }),
        ("Manufacturing", {
            "fields": ("mpn", "manufacturer", "footprint")
        }),
        ("Inventory Control", {
            "fields": ("low_stock_threshold", "default_storage", "is_default_storage_mandatory", "attrition_percent")
        }),
        ("Relations", {
            "fields": ("project", "meta_parts", "substitutes")
        }),
        ("Metadata", {
            "fields": ("tags", "cad_keys", "custom_fields")
        }),
    )
