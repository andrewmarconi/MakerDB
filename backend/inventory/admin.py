from django.contrib import admin
from .models import Storage, Lot, Stock

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

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
