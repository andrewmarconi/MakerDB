import os
import django
import sys

# Add backend directory to path
sys.path.append('backend')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makerdb.settings")
django.setup()

from inventory.models import Storage

location_id = "567f316c-54df-4e6c-9f18-69f29c6db1eb"
try:
    loc = Storage.objects.get(id=location_id)
    print(f"Location found: {loc.name}, Desc: {loc.description}, Tags: {loc.tags}")
    
    # Try updating
    old_name = loc.name
    new_name = loc.name + " (Test Update)"
    loc.name = new_name
    loc.save()
    
    # Check again
    loc_refreshed = Storage.objects.get(id=location_id)
    print(f"After update: {loc_refreshed.name}")
    
    if loc_refreshed.name == new_name:
        print("Persistence test PASSED in Django shell.")
    else:
        print("Persistence test FAILED in Django shell.")
    
    # Revert
    loc_refreshed.name = old_name
    loc_refreshed.save()
    print(f"Reverted to: {loc_refreshed.name}")

except Storage.DoesNotExist:
    print("Location NOT found")
except Exception as e:
    print(f"Error: {e}")
