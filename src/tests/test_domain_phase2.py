import pytest
from core.models import Company
from projects.models import Project
from procurement.models import Order, Offer
from parts.models import Part
from inventory.models import Lot

@pytest.mark.django_db
def test_project_creation():
    p = Project.objects.create(name="Robot Arm v1")
    assert str(p) == "Robot Arm v1"

@pytest.mark.django_db
def test_procurement_flow():
    # Vendor
    vendor = Company.objects.create(name="DigiKey", is_vendor=True)
    
    # Order
    order = Order.objects.create(vendor=vendor, number="PO-1234")
    assert str(order) == "DigiKey #PO-1234"
    
    # Lot linked to Order
    lot = Lot.objects.create(name="Batch 2025", order=order)
    assert lot.order == order

@pytest.mark.django_db
def test_part_linked_to_project():
    proj = Project.objects.create(name="Main Board")
    part = Part.objects.create(name="PCBA", project=proj, part_type=Part.PartType.SUB_ASSEMBLY)
    assert part.project == proj
