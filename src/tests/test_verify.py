import pytest
from django.urls import reverse
from core.models import Company

@pytest.mark.django_db
def test_admin_url_is_accessible(client):
    # Tests that /cp/ is the admin url
    url = "/cp/login/"
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_company_creation():
    c = Company.objects.create(name="Test Corp", is_vendor=True)
    assert c.name == "Test Corp"
    assert c.is_vendor is True
