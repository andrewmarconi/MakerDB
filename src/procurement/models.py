from django.db import models
from core.models import GlobalOpsBase, Attachment

class Order(GlobalOpsBase):
    """
    A Purchase Order or similar.
    """
    class OrderStatus(models.TextChoices):
        OPEN = "open", "Open"
        ORDERED = "ordered", "Ordered"
        RECEIVED = "received", "Received"

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
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.OPEN)
    
    attachments = models.ManyToManyField(Attachment, blank=True, related_name="orders")
    
    def __str__(self) -> str:
        return f"{self.vendor.name} #{self.number}"

class Offer(GlobalOpsBase):
    """
    A price offer from a vendor for a specific part.
    """
    class OfferType(models.TextChoices):
        LOCAL = "local", "Local"
        ONLINE = "online", "Online"
        SERVICE = "service", "Service"
    
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
    # Storing complex pricing in JSON.
    # Structure: { currency: 'USD', discounts: [{qty:1, amount: 0.10}] }
    prices = models.JSONField(default=list, blank=True) 
    
    in_stock_status = models.CharField(max_length=10, choices=InStockStatus.choices, null=True, blank=True)
    
    reference = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)
    url = models.URLField(max_length=2000, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Relations
    part = models.ForeignKey('parts.Part', on_delete=models.CASCADE, related_name="offers", null=True, blank=True)

    attachments = models.ManyToManyField(Attachment, blank=True, related_name="offers")

    def __str__(self) -> str:
        return f"{self.vendor.name}: {self.sku}" if self.vendor else f"Unknown Vendor: {self.sku}"
