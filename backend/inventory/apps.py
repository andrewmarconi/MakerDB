from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
    verbose_name = "Inventory"

    def ready(self):
        from core.typesense import StorageCollection
        from inventory.models import Storage

        collection = StorageCollection()
        collection.register(Storage)
