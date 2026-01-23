from django.core.management.base import BaseCommand
from inventory.models import Storage
from core.typesense import StorageCollection, registry


class Command(BaseCommand):
    help = "Sync Storage locations to Typesense"

    def handle(self, *args, **options):
        # Explicitly register and create the collection
        collection = StorageCollection()
        registry.register(collection)

        self.stdout.write("Creating Typesense collection...")
        collection.create_collection()

        self.stdout.write("Syncing existing Storage locations...")
        count = 0
        batch = []

        for storage in Storage.objects.all().iterator():
            doc = collection.to_document(storage)
            batch.append(doc)

            if len(batch) >= 100:
                # Upsert batch
                try:
                    registry.client.collections["storage"].documents.import_(batch)
                    count += len(batch)
                    self.stdout.write(f"Synced {count} locations...")
                    batch = []
                except Exception as e:
                    self.stderr.write(f"Batch sync error: {e}")

        # Final batch
        if batch:
            try:
                registry.client.collections["storage"].documents.import_(batch)
                count += len(batch)
            except Exception as e:
                self.stderr.write(f"Final batch sync error: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully synced {count} locations to Typesense"))
