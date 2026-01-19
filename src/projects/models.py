from django.db import models
from core.models import GlobalOpsBase, Attachment

class Project(GlobalOpsBase):
    """
    Represents a Project / BOM.
    """
    class ProjectStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.DRAFT)
    revision = models.CharField(max_length=50, default="1.0")
    
    attachments = models.ManyToManyField(Attachment, blank=True, related_name="projects")

    def __str__(self) -> str:
        return f"{self.name} (Rev {self.revision})"

class BOMItem(GlobalOpsBase):
    """
    An entry in a Project's BOM. Links a Part to a Project with a specific quantity.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bom_items")
    part = models.ForeignKey('parts.Part', on_delete=models.PROTECT, related_name="bom_usage")
    
    quantity = models.IntegerField(default=1)
    designators = models.TextField(blank=True, help_text="Comma-separated designators (e.g. R1, R2)")
    
    # Optional overrides
    substitutes = models.ManyToManyField('parts.Part', blank=True, related_name="bom_substitutes")
    
    class Meta(GlobalOpsBase.Meta):
        verbose_name = "BOM Item"
        verbose_name_plural = "BOM Items"

    def __str__(self) -> str:
        return f"{self.part.name} (x{self.quantity}) for {self.project.name}"
