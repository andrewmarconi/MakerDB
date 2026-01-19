from django.db import models
from core.models import GlobalOpsBase, Attachment

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
