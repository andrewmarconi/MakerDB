from django.db import models
from django.db.models import Sum
from core.models import GlobalOpsBase, Attachment

class Part(GlobalOpsBase):
    """
    The core component model.
    """
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
    
    mpn = models.CharField(max_length=255, blank=True, verbose_name="Manufacturer Part Number")
    
    cad_keys = models.JSONField(default=list, blank=True) # List[str]
    
    # Inventory Control
    low_stock_threshold = models.IntegerField(null=True, blank=True)
    attrition_percent = models.FloatField(default=0.0)
    attrition_quantity = models.IntegerField(default=0)
    
    default_storage = models.ForeignKey(
        'inventory.Storage', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="default_for_parts"
    )
    is_default_storage_mandatory = models.BooleanField(default=False)
    
    # Relations
    # Meta parts group other parts
    meta_parts = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="meta_parents")
    # Substitute parts
    substitutes = models.ManyToManyField("self", blank=True, symmetrical=True, related_name="substituted_by")
    
    # If sub-assembly, links to a Project
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name="part_assemblies")

    attachments = models.ManyToManyField(Attachment, blank=True, related_name="parts")

    @property
    def total_stock(self) -> int:
        """
        Calculates the total on-hand stock for this part.
        On-hand stock is defined as Stock entries where status is None (meaning available).
        """
        # We filter for status__isnull=True because the API defines "no status" as on-hand stock.
        result = self.stock_entries.filter(status__isnull=True).aggregate(total=Sum('quantity'))
        return result['total'] or 0

    def __str__(self) -> str:
        return f"{self.name} ({self.mpn})" if self.mpn else self.name
