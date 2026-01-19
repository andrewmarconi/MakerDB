import uuid
from django.db import models

class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    """ 
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
    
    # Storage URL or generic FileField would go here.
    # For now, we stub it or use a simple FileField if needed, but the schema doesn't strictly require it yet.
    # We'll add a file field for completeness.
    file = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.filename
