from django.contrib import admin
from django.db.models import Sum
from .models import Storage, Lot, Stock

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_parts', 'description')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_total_parts=Sum("stock_in_location__quantity"))

    @admin.display(description="Total Parts")
    def total_parts(self, obj):
        return obj._total_parts or 0

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('name', 'expiration_date', 'order')
    search_fields = ('name',)
    filter_horizontal = ('attachments',) # Assuming ManyToMany interface

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('part', 'quantity', 'storage', 'lot', 'status')
    search_fields = ('part__name', 'storage__name', 'lot__name')
    list_filter = ('status', 'storage')
