"""
Sync storage locations to Typesense search index.
Recreates the collection with proper schema for substring matching.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import Storage
import httpx
import socket


class Command(BaseCommand):
    help = "Sync storage locations to Typesense search index"

    def get_typesense_config(self):
        """Get Typesense configuration."""
        try:
            socket.gethostbyname("typesense")
            host = "typesense"
        except socket.gaierror:
            host = "localhost"

        return {"url": f"http://{host}:8108", "api_key": settings.TYPESENSE_API_KEY}

    def handle(self, *args, **options):
        config = self.get_typesense_config()
        headers = {"X-TYPESENSE-API-KEY": config["api_key"]}

        self.stdout.write("Connecting to Typesense at {}...".format(config["url"]))

        with httpx.Client(timeout=30.0) as client:
            # Delete existing collection if it exists
            self.stdout.write("Deleting existing collection...")
            try:
                response = client.delete(f"{config['url']}/collections/storage", headers=headers)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS("✓ Deleted existing collection"))
                elif response.status_code == 404:
                    self.stdout.write("Collection doesn't exist yet, creating new...")
                else:
                    self.stdout.write(self.style.WARNING(f"Unexpected response: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error deleting collection: {e}"))

            # Create new collection with infix search enabled
            self.stdout.write("Creating new collection with infix search...")
            schema = {
                "name": "storage",
                "fields": [
                    {"name": "id", "type": "string"},
                    {"name": "name", "type": "string", "infix": True},
                    {"name": "description", "type": "string", "optional": True, "infix": True},
                    {"name": "parent_id", "type": "string", "optional": True},
                    {"name": "created_at", "type": "int64"},
                ],
                "default_sorting_field": "created_at",
            }

            try:
                response = client.post(f"{config['url']}/collections", headers=headers, json=schema)
                response.raise_for_status()
                self.stdout.write(self.style.SUCCESS("✓ Created collection with infix search enabled"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating collection: {e}"))
                if hasattr(e, 'response'):
                    self.stdout.write(self.style.ERROR(f"Response: {e.response.text}"))
                return

            # Index all storage locations
            self.stdout.write("Indexing storage locations...")
            locations = Storage.objects.all()
            total = locations.count()
            self.stdout.write(f"Found {total} locations to index")

            indexed = 0
            failed = 0

            for location in locations:
                doc = {
                    "id": str(location.id),
                    "name": location.name,
                    "description": location.description or "",
                    "parent_id": str(location.parent_id) if location.parent_id else "",
                    "created_at": int(location.created_at.timestamp()),
                }

                try:
                    response = client.post(
                        f"{config['url']}/collections/storage/documents", headers=headers, json=doc
                    )
                    response.raise_for_status()
                    indexed += 1
                    if indexed % 50 == 0:
                        self.stdout.write(f"Indexed {indexed}/{total}...")
                except Exception as e:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"Failed to index {location.name}: {e}"))

            self.stdout.write(self.style.SUCCESS(f"\n✓ Indexing complete!"))
            self.stdout.write(f"  Indexed: {indexed}")
            if failed > 0:
                self.stdout.write(self.style.WARNING(f"  Failed: {failed}"))
