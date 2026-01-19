from django.contrib import admin
from .models import Order, Offer
from inventory.models import Lot

class LotInline(admin.TabularInline):
    model = Lot
    fields = ('name', 'description')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'vendor', 'po_number', 'expected_arrival')
    search_fields = ('number', 'vendor__name', 'po_number')
    list_filter = ('vendor',)
    
    inlines = [LotInline]
    
    fieldsets = (
        ("Details", {
            "fields": ("vendor", "number", "po_number", "invoice_number")
        }),
        ("Dates", {
            "fields": ("expected_arrival",)
        }),
        ("Notes", {
            "fields": ("notes", "comments")
        }),
    )

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('sku', 'vendor', 'part', 'moq', 'offer_type')
    search_fields = ('sku', 'vendor__name', 'part__name')
    list_filter = ('vendor', 'offer_type')
