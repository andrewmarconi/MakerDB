from django.db import models
from core.models import GlobalOpsBase, Attachment

class Storage(GlobalOpsBase):
    """
    Represents a physical storage location (e.g., 'Shelf A', 'Bin 1').
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    attachments = models.ManyToManyField(Attachment, blank=True, related_name="storages")

    class Meta(GlobalOpsBase.Meta):
        verbose_name_plural = "Storage"

    def __str__(self) -> str:
        return self.name

class Lot(GlobalOpsBase):
    """
    Represents a specific batch of parts.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    
    # Link to Order is optional but helpful to trace origin.
    order = models.ForeignKey('procurement.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name="lots")

    def __str__(self) -> str:
        return self.name

class Stock(GlobalOpsBase):
    """
    Corresponds to 'PartSource' or 'StockEntry'.
    Joins Part + Storage + Lot.
    """
    class StockStatus(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        RESERVED = "reserved", "Reserved"
        ALLOCATED = "allocated", "Allocated"
        IN_PRODUCTION = "in-production", "In Production"
        IN_TRANSIT = "in-transit", "In Transit"
        PLANNED = "planned", "Planned"
        REJECTED = "rejected", "Rejected"
        BEING_ORDERED = "being-ordered", "Being Ordered"
        AVAILABLE = "available", "Available" # Implicit default if none

    # We reference Part by string to avoid circular dependency
    part = models.ForeignKey('parts.Part', on_delete=models.CASCADE, related_name="stock_entries")
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT, related_name="stock_in_location")
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_entries")
    
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=StockStatus.choices, null=True, blank=True)
    
    # Tracking - Inherited from GlobalOpsBase (created_at/updated_at), 
    # but schema asked for first_seen/last_seen. 
    # We can rely on created_at/updated_at or add explicit fields if they mean something different.
    # Schema had:
    # first_seen = models.DateTimeField(auto_now_add=True)
    # last_seen = models.DateTimeField(auto_now=True)
    # These are effectively duplicates of TimeStampedModel fields. I'll omit them or map them.
    
    price_unit = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True) # ISO code
    
    class Meta(GlobalOpsBase.Meta):
        indexes = [] 
        verbose_name_plural = "Stock"
