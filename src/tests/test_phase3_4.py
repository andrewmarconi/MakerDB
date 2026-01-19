import pytest
from projects.models import Project, BOMItem
from parts.models import Part
from procurement.models import Order
from inventory.models import Lot
from core.models import Attachment, Company

@pytest.mark.django_db
def test_project_bom_phase3():
    """Verify Project status, revision, and BOM Items."""
    # Create Project
    proj = Project.objects.create(
        name="Test Device",
        revision="B",
        status=Project.ProjectStatus.ACTIVE,
        description="A test project"
    )
    assert proj.status == "active"
    assert proj.revision == "B"
    assert str(proj) == "Test Device (Rev B)"
    
    # Create Part
    part = Part.objects.create(name="Resistor 10k", part_type="local")
    
    # Create BOM Item
    bom_item = BOMItem.objects.create(
        project=proj,
        part=part,
        quantity=5,
        designators="R1, R2, R3, R4, R5"
    )
    
    assert bom_item.project == proj
    assert bom_item.part == part
    assert bom_item.quantity == 5
    assert proj.bom_items.count() == 1
    assert part.bom_usage.count() == 1

@pytest.mark.django_db
def test_procurement_phase4():
    """Verify Order status and attachments."""
    vendor = Company.objects.create(name="DigiKey", is_vendor=True)
    
    # Order
    order = Order.objects.create(
        vendor=vendor,
        number="PO-12345",
        status=Order.OrderStatus.ORDERED
    )
    assert order.status == "ordered"
    
    # Attachment
    att = Attachment.objects.create(filename="invoice.pdf", file_type="invoice")
    order.attachments.add(att)
    assert order.attachments.count() == 1
    assert order.attachments.first() == att

@pytest.mark.django_db
def test_inventory_lot_attachments_phase4():
    """Verify Lot attachments."""
    # Create Lot
    lot = Lot.objects.create(name="Lot-2023-A")
    
    # Attachment
    att = Attachment.objects.create(filename="test_report.pdf", file_type="other")
    lot.attachments.add(att)
    
    assert lot.attachments.count() == 1
