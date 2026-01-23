"""
Typesense integration for Django models.
Provides real-time sync via Django signals.
"""

import os
from typing import Any, Dict, List, Optional
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.db import models
import typesense


class TypesenseRegistry:
    """Registry for managing Typesense collections."""

    def __init__(self):
        self.collections: Dict[str, "TypesenseCollection"] = {}
        self._client: Optional[typesense.Client] = None

    @property
    def client(self) -> typesense.Client:
        if self._client is None:
            # Check if running inside Docker (typesense hostname resolves)
            # Otherwise use localhost for host-based connections
            import socket

            try:
                socket.gethostbyname("typesense")
                host = "typesense"
            except socket.gaierror:
                host = "localhost"

            self._client = typesense.Client(
                {
                    "api_key": os.getenv("TYPESENSE_API_KEY", "secret"),
                    "nodes": [
                        {
                            "host": host,
                            "port": os.getenv("TYPESENSE_PORT", "8108"),
                            "protocol": os.getenv("TYPESENSE_PROTOCOL", "http"),
                        }
                    ],
                    "connection_timeout_seconds": 2,
                }
            )
        return self._client

    def register(self, collection: "TypesenseCollection"):
        """Register a collection for auto-sync."""
        self.collections[collection.name] = collection

    def sync_model(self, instance: models.Model):
        """Sync a model instance to Typesense."""
        collection_name = getattr(instance, "_typesense_collection", None)
        if not collection_name:
            return

        coll = self.collections.get(collection_name)
        if not coll:
            return

        doc = coll.to_document(instance)
        try:
            self.client.collections[collection_name].documents.upsert(doc)
        except Exception as e:
            print(f"Typesense sync error for {collection_name}: {e}")

    def delete_model(self, instance: models.Model):
        """Delete a model instance from Typesense."""
        collection_name = getattr(instance, "_typesense_collection", None)
        if not collection_name:
            return

        try:
            self.client.collections[collection_name].documents[str(instance.id)].delete()
        except Exception as e:
            print(f"Typesense delete error for {collection_name}: {e}")


registry = TypesenseRegistry()


class TypesenseCollection:
    """Base class for Typesense collections."""

    name: str = ""
    schema: Dict[str, Any] = {}
    query_by_fields: List[str] = []

    def to_document(self, instance: models.Model) -> Dict[str, Any]:
        """Convert Django model to Typesense document."""
        raise NotImplementedError

    def register(self, model_class: type[models.Model]):
        """Register this collection for a Django model."""
        model_class._typesense_collection = self.name
        registry.register(self)

        # Connect signals
        post_save.connect(self._handle_save, sender=model_class)
        post_delete.connect(self._handle_delete, sender=model_class)

    def _handle_save(self, sender, instance, created, **kwargs):
        registry.sync_model(instance)

    def _handle_delete(self, sender, instance, **kwargs):
        registry.delete_model(instance)

    def create_collection(self):
        """Create the collection in Typesense if it doesn't exist."""
        try:
            self.client.collections.create(
                {
                    "name": self.name,
                    "fields": self._get_schema_fields(),
                    "default_sorting_field": "created_at",
                }
            )
        except Exception as e:
            print(f"Collection {self.name} creation: {e}")

    def _get_schema_fields(self) -> List[Dict[str, Any]]:
        """Generate schema fields from collection schema."""
        fields = [
            {"name": "id", "type": "string", "optional": False},
        ]
        for field_name, field_type in self.schema.items():
            type_map = {
                str: "string",
                int: "int64",
                float: "float",
                bool: "bool",
            }
            fields.append(
                {
                    "name": field_name,
                    "type": type_map.get(field_type, "string"),
                    "optional": True,
                }
            )
        # Add created_at as non-optional for default sorting (not in schema dict)
        fields.append({"name": "created_at", "type": "int64", "optional": False})
        return fields

    @property
    def client(self) -> typesense.Client:
        return registry.client


class StorageCollection(TypesenseCollection):
    """Typesense collection for Storage locations."""

    name = "storage"
    query_by_fields = ["name", "description"]

    schema = {
        "name": str,
        "description": str,
        "parent_id": str,
    }

    def to_document(self, instance) -> Dict[str, Any]:
        return {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description or "",
            "parent_id": str(instance.parent_id) if instance.parent_id else "",
            "created_at": int(instance.created_at.timestamp()) if instance.created_at else 0,
        }


def setup_typesense_sync():
    """Set up Typesense sync for all registered collections."""
    for collection in registry.collections.values():
        collection.create_collection()
