"""
Django Schema Design
Python 3.12+ / Django 6.x

This file documents the proposed database schema and app structure for the MakerDB project.

Proposed App Structure:
1. core: Common utilities, base models, attachments.
2. parts: Part management and definitions.
3. inventory: Stock, lots, storage locations.
4. projects: Projects and BOMs.
5. procurement: Orders, offers, and supplier data.

Note regarding typing:
- We use Python 3.12 type hinting.
- Django models are typed using `django-stubs` conventions where applicable.
"""

import uuid
from decimal import Decimal
from typing import List, Optional, Any
from enum import Enum, unique
from datetime import datetime

# In a real Django project, these would be imported from django.db
# Mocking for schema design purposes
class models:
    class Model: pass
    class TextChoices(Enum): pass
    
    class UUIDField:
        def __init__(self, primary_key: bool = False, default: Any = None, editable: bool = True): pass
    class CharField:
        def __init__(self, max_length: int, blank: bool = False, null: bool = False, choices: Any = None): pass
    class TextField:
        def __init__(self, blank: bool = False, null: bool = False): pass
    class IntegerField:
        def __init__(self, default: int = 0, null: bool = False): pass
    class FloatField:
        def __init__(self, default: float = 0.0): pass
    class DecimalField:
        def __init__(self, max_digits: int, decimal_places: int, null: bool = False, blank: bool = False): pass
    class BooleanField:
        def __init__(self, default: bool = False): pass
    class DateTimeField:
        def __init__(self, auto_now_add: bool = False, null: bool = False, blank: bool = False): pass
    class JSONField:
        def __init__(self, default: Any = dict, blank: bool = True): pass
    class ForeignKey:
        def __init__(self, to: Any, on_delete: Any, related_name: str, null: bool = False, blank: bool = False, limit_choices_to: Any = None): pass
    class ManyToManyField:
        def __init__(self, to: Any, blank: bool = False, related_name: str = None, symmetrical: bool = False): pass
    class Sum:
        def __init__(str): pass
    
    CASCADE = "CASCADE"
    PROTECT = "PROTECT"
    SET_NULL = "SET_NULL"

# =============================================================================
# APP: CORE
# =============================================================================

class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating
    'created' and 'modified' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Implied functionality for schema

    class Meta:
        abstract = True

class GlobalOpsBase(TimeStampedModel):
    """
    Abstract base class for main entities (Part, Project, etc.)
    that share common fields like UUID, keys, descriptions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Common metadata
    tags = models.JSONField(default=list, blank=True)  # List[str]
    custom_fields = models.JSONField(default=dict, blank=True)  # Record<str, str>
    
    class Meta:
        abstract = True

class Company(GlobalOpsBase):
    """
    Represents a third-party entity, such as a Manufacturer or Vendor/Supplier.
    Normalized to ensure data consistency across Parts and Orders.
    """
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    is_manufacturer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    
    contacts = models.JSONField(default=list, blank=True) # List of contact info objects

    def __str__(self) -> str:
        return self.name

class Attachment(TimeStampedModel):
    """
    Represents an attachment (image, datasheet, etc.).
    In a real implementation, this might use GenericForeignKey to attach to any object
    (Part, Project, Order), or specific foreign keys if queries need optimization.
    Thinking about the API, it seems widely used.
    """ 
    @unique
    class AttachmentType(models.TextChoices):
        IMAGE = "image", "Image"
        DATASHEET = "datasheet", "Datasheet"
        CAD = "cad", "CAD File"
        GERBERS = "gerbers", "Gerbers"
        KICAD_PCB = "kicad-pcb", "KiCad PCB"
        EAGLE_BRD = "eagle-brd", "Eagle Board"
        INVOICE = "invoice", "Invoice"
        PURCHASE_ORDER = "purchase-order", "Purchase Order"
        SHIPPING_LIST = "shipping-list", "Shipping List"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_type = models.CharField(max_length=20, choices=AttachmentType.choices, default=AttachmentType.OTHER)
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100) # MIME type
    size = models.IntegerField(default=0) # Bytes
    
    # Storage URL or generic FileField would go here
    # file = models.FileField(upload_to='attachments/')

    class Meta:
        indexes = [] # Add generic index if using GFK

# =============================================================================
# APP: INVENTORY (Storage, Lots)
# =============================================================================

class Storage(GlobalOpsBase):
    """
    Represents a physical storage location (e.g., 'Shelf A', 'Bin 1').
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Attachments can be linked via a ManyToMany or GenericRelation
    attachments = models.ManyToManyField(Attachment, blank=True, related_name="storages")

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
    
    # Link to Order is optional but helpful to trace origin
    # defined as string in TS, likely an ID to Order
    # order = models.ForeignKey('procurement.Order', ...)

    def __str__(self) -> str:
        return self.name

# =============================================================================
# APP: PARTS
# =============================================================================

class Part(GlobalOpsBase):
    """
    The core component model.
    """
    @unique
    class PartType(models.TextChoices):
        SUB_ASSEMBLY = "sub-assembly", "Sub-Assembly"
        META = "meta", "Meta-Part"
        LINKED = "linked", "Linked Part"
        LOCAL = "local", "Local Part"

    part_type = models.CharField(max_length=20, choices=PartType.choices, default=PartType.LOCAL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Markdown supported")
    
    footprint = models.CharField(max_length=255, blank=True)
    
    # Normalized Manufacturer
    manufacturer = models.ForeignKey(
        'core.Company', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="manufactured_parts",
        limit_choices_to={'is_manufacturer': True}
    )
    # manufacturer_name kept for fallback/import if needed, or removed if strict.
    # We will assume strict normalization here, but often good to keep a "raw" field during migration.
    
    mpn = models.CharField(max_length=255, blank=True, verbose_name="Manufacturer Part Number")
    
    cad_keys = models.JSONField(default=list, blank=True) # List[str]
    
    # Inventory Control
    low_stock_threshold = models.IntegerField(null=True, blank=True)
    attrition_percent = models.FloatField(default=0.0)
    attrition_quantity = models.IntegerField(default=0)
    
    default_storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True, related_name="default_for_parts")
    is_default_storage_mandatory = models.BooleanField(default=False)
    
    # Relations
    # Meta parts group other parts
    meta_parts = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="meta_parents")
    # Substitute parts
    substitutes = models.ManyToManyField("self", blank=True, symmetrical=True, related_name="substituted_by")
    
    # If sub-assembly, links to a Project
    project_id_ref = models.UUIDField(null=True, blank=True) # ForeignKey to Project locally if needed

    attachments = models.ManyToManyField(Attachment, blank=True, related_name="parts")

    @property
    def total_stock(self) -> int:
        """
        Calculates the total on-hand stock for this part.
        On-hand stock is defined as Stock entries where status is None (meaning available).
        """
        # In a real Django app, you would import Sum
        # from django.db.models import Sum
        
        # We filter for status__isnull=True because the API defines "no status" as on-hand stock.
        # Entries with status 'ordered', 'reserved', etc. are not counted in available stock.
        result = self.stock_entries.filter(status__isnull=True).aggregate(total=models.Sum('quantity'))
        return result['total'] or 0

    def __str__(self) -> str:
        return f"{self.name} ({self.mpn})" if self.mpn else self.name


class Stock(GlobalOpsBase):
    """
    Corresponds to 'PartSource' or 'StockEntry'.
    Joins Part + Storage + Lot.
    """
    @unique
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

    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="stock_entries")
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT, related_name="stock_in_location")
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_entries")
    
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=StockStatus.choices, null=True, blank=True)
    
    # Tracking
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    # Additional financial data sometimes stored on stock entry
    price_unit = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True) # ISO code
    
    class Meta:
        indexes = [] # Composite index on part, storage, lot often useful

# =============================================================================
# APP: PROJECTS
# =============================================================================

class Project(GlobalOpsBase):
    """
    Represents a Project / BOM.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    attachments = models.ManyToManyField(Attachment, blank=True, related_name="projects")

    def __str__(self) -> str:
        return self.name

# =============================================================================
# APP: PROCUREMENT (Orders, Offers)
# =============================================================================

class Order(GlobalOpsBase):
    """
    A Purchase Order or similar.
    """
    # Normalized Vendor
    vendor = models.ForeignKey(
        'core.Company', 
        on_delete=models.PROTECT, 
        related_name="orders",
        limit_choices_to={'is_vendor': True}
    )
    
    number = models.CharField(max_length=255, help_text="Vendor Order Number")
    invoice_number = models.CharField(max_length=255, blank=True)
    po_number = models.CharField(max_length=255, blank=True, help_text="Internal PO Number")
    
    comments = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    expected_arrival = models.DateTimeField(null=True, blank=True)
    
    # In a full app, OrderEntries would link Part -> Order
    
    def __str__(self) -> str:
        return f"{self.vendor.name} #{self.number}"

class Offer(GlobalOpsBase):
    """
    A price offer from a vendor for a specific part.
    """
    @unique
    class OfferType(models.TextChoices):
        LOCAL = "local", "Local"
        ONLINE = "online", "Online"
        SERVICE = "service", "Service"
    
    @unique
    class InStockStatus(models.TextChoices):
        YES = "yes", "Yes"
        NO = "no", "No"
        MAYBE = "maybe", "Maybe"
        ASSUMED = "assumed", "Assumed"

    offer_type = models.CharField(max_length=20, choices=OfferType.choices, default=OfferType.LOCAL)
    
    # Normalized Vendor
    vendor = models.ForeignKey(
        'core.Company', 
        on_delete=models.CASCADE, 
        related_name="offers",
        null=True, 
        blank=True,
        limit_choices_to={'is_vendor': True}
    )
    
    sku = models.CharField(max_length=255, blank=True, help_text="Vendor SKU")
    
    # Quantities
    moq = models.IntegerField(default=1, verbose_name="Minimum Order Quantity")
    order_multiple = models.IntegerField(default=1)
    
    # Pricing
    # prices = PriceStructure[] in TS.
    # Storing complex pricing steps in JSON is often easier than a separate EAV table 
    # unless you need to query "all parts with price < X" efficiently.
    # Given structure { currency: 'USD', discounts: [{qty:1, amount: 0.10}] }
    prices = models.JSONField(default=list, blank=True) 
    
    in_stock_status = models.CharField(max_length=10, choices=InStockStatus.choices, null=True, blank=True)
    
    reference = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)
    url = models.URLField(max_length=2000, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Relations
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="offers", null=True, blank=True)
    # entry_id ref could go here if needed

    attachments = models.ManyToManyField(Attachment, blank=True, related_name="offers")

    def __str__(self) -> str:
        return f"{self.vendor.name}: {self.sku}" if self.vendor else f"Unknown Vendor: {self.sku}"
