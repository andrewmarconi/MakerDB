from typing import List
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from pydantic import BaseModel
from inventory.models import Storage, Lot, Stock
from inventory.schemas import (
    StorageSchema,
    StorageCreate,
    StorageUpdate,
    LotSchema,
    LotCreate,
    LotUpdate,
    StockSchema,
    StockCreate,
    StockUpdate,
)
from parts.models import Part
from procurement.models import Order
from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Exists, OuterRef, Sum
import logging


class LowStockAlert(BaseModel):
    id: UUID
    name: str
    mpn: str
    stock: int
    min: int
    status: str


class StorageOccupancyItem(BaseModel):
    name: str
    quantity: int


class StorageOccupancySummary(BaseModel):
    total_locations: int
    used_locations: int
    empty_locations: int
    used_percentage: float
    top_locations: List[StorageOccupancyItem]


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# --- Storage Location Endpoints ---


def _get_storage_queryset():
    return Storage.objects.prefetch_related("attachments")


@router.get("/locations", response_model=List[StorageSchema])
async def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    has_stock: bool = Query(None, description="Filter by stock status (true=has stock, false=empty)"),
    parent_id: UUID = Query(None, description="Filter by parent location"),
    tags: str = Query(None, description="Filter by tags (comma-separated)"),
):
    """
    List storage locations with optional filters.
    For search, use /search/locations endpoint instead.
    """

    @sync_to_async
    def _list_locations():
        queryset = _get_storage_queryset()

        # Apply filters
        if has_stock is not None:
            if has_stock:
                # Locations that have at least one stock entry with quantity > 0
                queryset = queryset.filter(stock_in_location__quantity__gt=0).distinct()
            else:
                # Locations that have no stock entries OR only stock entries with quantity = 0
                has_stock_subquery = Stock.objects.filter(storage_id=OuterRef("pk"), quantity__gt=0)
                queryset = queryset.exclude(Exists(has_stock_subquery))

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=[tag])

        locations = list(queryset[skip : skip + limit])

        # Eagerly convert attachments to lists
        for location in locations:
            location.__dict__['attachments'] = list(location.attachments.all())

        return locations

    locations = await _list_locations()
    return locations


@router.get("/locations/count", response_model=dict)
async def count_locations(
    has_stock: bool = Query(None, description="Filter by stock status (true=has stock, false=empty)"),
    parent_id: UUID = Query(None, description="Filter by parent location"),
    tags: str = Query(None, description="Filter by tags (comma-separated)"),
):
    """
    Count storage locations with optional filters.
    For search, use /search/locations endpoint which includes count in response.
    """

    @sync_to_async
    def _count_locations():
        queryset = _get_storage_queryset()

        # Apply same filters as list_locations
        if has_stock is not None:
            if has_stock:
                queryset = queryset.filter(stock_in_location__quantity__gt=0).distinct()
            else:
                has_stock_subquery = Stock.objects.filter(storage_id=OuterRef("pk"), quantity__gt=0)
                queryset = queryset.exclude(Exists(has_stock_subquery))

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=[tag])

        return queryset.count()

    count = await _count_locations()
    return {"count": count}


@router.get("/locations/{location_id}", response_model=StorageSchema)
async def get_location(location_id: UUID):
    @sync_to_async
    def _get():
        try:
            location = _get_storage_queryset().get(id=location_id)
            # Eagerly convert attachments to lists
            location.__dict__['attachments'] = list(location.attachments.all())
            return location
        except Storage.DoesNotExist:
            return None

    location = await _get()
    if location is None:
        raise HTTPException(status_code=404, detail="Storage location not found")
    return location


@router.post("/locations", response_model=StorageSchema, status_code=201)
async def create_location(data: StorageCreate):
    """Create a new storage location."""

    @sync_to_async
    def _create():
        location = Storage.objects.create(**data.model_dump())
        location = _get_storage_queryset().get(id=location.id)
        # Eagerly convert attachments to lists
        location.__dict__['attachments'] = list(location.attachments.all())
        return location

    location = await _create()
    return location


@router.put("/locations/{location_id}", response_model=StorageSchema)
async def update_location(location_id: UUID, data: StorageUpdate):
    """Update a storage location."""

    @sync_to_async
    def _update():
        try:
            logger.info(f"Starting atomic update for location {location_id}")
            with transaction.atomic():
                try:
                    location = Storage.objects.select_for_update().get(id=location_id)
                    logger.debug(f"Acquired lock on location {location_id}")
                except Storage.DoesNotExist:
                    raise ValueError("Storage location not found", 404)

                update_data = data.model_dump(exclude_unset=True)
                logger.info(f"Updating location {location_id} with data: {update_data}")

                for field, value in update_data.items():
                    setattr(location, field, value)

                location.save()
                logger.debug(f"Saved location {location_id}")

                # Refresh from DB to ensure we returning the current state
                updated = _get_storage_queryset().get(id=location.id)
                # Eagerly convert attachments to lists
                updated.__dict__['attachments'] = list(updated.attachments.all())
                logger.info(f"Successfully updated location {location_id}")
                return updated
        except Exception as e:
            logger.error(f"Error updating location {location_id}: {e}")
            raise

    try:
        location = await _update()
        return location
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/locations/{location_id}", status_code=204)
async def delete_location(location_id: UUID):
    """Delete a storage location."""

    @sync_to_async
    def _delete():
        try:
            location = Storage.objects.get(id=location_id)
            # Check if location has stock entries
            if location.stock_in_location.exists():
                raise ValueError("Cannot delete location with stock entries", 400)
            location.delete()
            return True
        except Storage.DoesNotExist:
            return False

    try:
        deleted = await _delete()
        if not deleted:
            raise HTTPException(status_code=404, detail="Storage location not found")
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


# --- Stock Endpoints ---


def _get_stock_queryset():
    return Stock.objects.select_related(
        "part__manufacturer",
        "part__default_storage",
        "part__project",
        "storage",
        "lot"
    ).prefetch_related(
        "storage__attachments",
        "lot__attachments",
        "part__attachments"
    )


@router.get("/stock", response_model=List[StockSchema])
async def list_stock(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    @sync_to_async
    def _list():
        from django.db.models import Sum

        stock_items = list(_get_stock_queryset().all()[skip : skip + limit])

        # Calculate total_stock for all parts at once
        part_ids = [stock.part_id for stock in stock_items if stock.part_id]
        if part_ids:
            part_totals = dict(
                Stock.objects.filter(
                    part_id__in=part_ids,
                    status__isnull=True
                )
                .values('part_id')
                .annotate(total=Sum('quantity'))
                .values_list('part_id', 'total')
            )
        else:
            part_totals = {}

        # Eagerly convert attachments and add total_stock
        for stock in stock_items:
            if stock.storage:
                stock.storage.__dict__['attachments'] = list(stock.storage.attachments.all())
            if stock.lot:
                stock.lot.__dict__['attachments'] = list(stock.lot.attachments.all())
            if stock.part:
                stock.part.__dict__['attachments'] = list(stock.part.attachments.all())
                stock.part.total_stock = part_totals.get(stock.part.id, 0)

        return stock_items

    return await _list()


@router.get("/locations/{location_id}/stock", response_model=List[StockSchema])
async def get_stock_by_location(location_id: UUID):
    """Get all stock entries for a specific location."""

    @sync_to_async
    def _get_stock():
        from django.db.models import Sum, Q

        try:
            location = Storage.objects.get(id=location_id)
        except Storage.DoesNotExist:
            return None

        stock_items = list(
            Stock.objects.filter(storage=location)
            .select_related(
                "part__manufacturer",
                "part__default_storage",
                "part__project",
                "storage",
                "lot"
            )
            .prefetch_related(
                "storage__attachments",
                "lot__attachments",
                "part__attachments"
            )
            .all()
        )

        # Calculate total_stock for all parts at once (avoid N+1 queries)
        part_ids = [stock.part_id for stock in stock_items if stock.part_id]
        if part_ids:
            part_totals = dict(
                Stock.objects.filter(
                    part_id__in=part_ids,
                    status__isnull=True
                )
                .values('part_id')
                .annotate(total=Sum('quantity'))
                .values_list('part_id', 'total')
            )
        else:
            part_totals = {}

        # Eagerly convert attachments to lists to avoid async context issues
        # We replace the ManyRelatedManager with a list so Pydantic doesn't try to query it
        for stock in stock_items:
            if stock.storage:
                attachments_list = list(stock.storage.attachments.all())
                stock.storage.__dict__['attachments'] = attachments_list
            if stock.lot:
                attachments_list = list(stock.lot.attachments.all())
                stock.lot.__dict__['attachments'] = attachments_list
            if stock.part:
                attachments_list = list(stock.part.attachments.all())
                stock.part.__dict__['attachments'] = attachments_list
                # Add total_stock from pre-calculated totals
                stock.part.total_stock = part_totals.get(stock.part.id, 0)

        return stock_items

    stock = await _get_stock()
    if stock is None:
        raise HTTPException(status_code=404, detail="Storage location not found")

    return stock


@router.get("/stock/count", response_model=dict)
async def count_stock():
    count = await sync_to_async(_get_stock_queryset().count)()
    return {"count": count}


@router.get("/stock/{stock_id}", response_model=StockSchema)
async def get_stock(stock_id: UUID):
    @sync_to_async
    def _get():
        from django.db.models import Sum

        try:
            stock = _get_stock_queryset().get(id=stock_id)
        except Stock.DoesNotExist:
            return None

        # Eagerly convert attachments
        if stock.storage:
            stock.storage.__dict__['attachments'] = list(stock.storage.attachments.all())
        if stock.lot:
            stock.lot.__dict__['attachments'] = list(stock.lot.attachments.all())
        if stock.part:
            stock.part.__dict__['attachments'] = list(stock.part.attachments.all())
            # Calculate total_stock for this part
            total = Stock.objects.filter(
                part=stock.part,
                status__isnull=True
            ).aggregate(total=Sum('quantity'))['total'] or 0
            stock.part.total_stock = total

        return stock

    stock = await _get()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    return stock


@router.post("/stock", response_model=StockSchema, status_code=201)
async def create_stock(data: StockCreate):
    """Create a new stock entry."""

    @sync_to_async
    def _create():
        # Validate part exists
        try:
            part = Part.objects.get(id=data.part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 400)

        # Validate storage exists
        try:
            storage = Storage.objects.get(id=data.storage_id)
        except Storage.DoesNotExist:
            raise ValueError("Storage location not found", 400)

        # Validate lot if provided
        lot = None
        if data.lot_id:
            try:
                lot = Lot.objects.get(id=data.lot_id)
            except Lot.DoesNotExist:
                raise ValueError("Lot not found", 400)

        from django.db.models import Sum

        stock_data = data.model_dump(exclude={"part_id", "storage_id", "lot_id"})
        stock = Stock.objects.create(part=part, storage=storage, lot=lot, **stock_data)
        stock = _get_stock_queryset().get(id=stock.id)

        # Eagerly convert attachments
        if stock.storage:
            stock.storage.__dict__['attachments'] = list(stock.storage.attachments.all())
        if stock.lot:
            stock.lot.__dict__['attachments'] = list(stock.lot.attachments.all())
        if stock.part:
            stock.part.__dict__['attachments'] = list(stock.part.attachments.all())
            # Calculate total_stock
            total = Stock.objects.filter(
                part=stock.part,
                status__isnull=True
            ).aggregate(total=Sum('quantity'))['total'] or 0
            stock.part.total_stock = total

        return stock

    try:
        stock = await _create()
        return stock
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.put("/stock/{stock_id}", response_model=StockSchema)
async def update_stock(stock_id: UUID, data: StockUpdate):
    """Update a stock entry (adjust quantity, change status, etc.)."""

    @sync_to_async
    def _update():
        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            raise ValueError("Stock entry not found", 404)

        update_data = data.model_dump(exclude_unset=True)

        # Handle foreign key fields
        if "storage_id" in update_data:
            storage_id = update_data.pop("storage_id")
            try:
                stock.storage = Storage.objects.get(id=storage_id)
            except Storage.DoesNotExist:
                raise ValueError("Storage location not found", 400)

        if "lot_id" in update_data:
            lot_id = update_data.pop("lot_id")
            if lot_id is None:
                stock.lot = None
            else:
                try:
                    stock.lot = Lot.objects.get(id=lot_id)
                except Lot.DoesNotExist:
                    raise ValueError("Lot not found", 400)

        # Update remaining fields
        for field, value in update_data.items():
            setattr(stock, field, value)

        stock.save()
        stock = _get_stock_queryset().get(id=stock.id)

        # Eagerly convert attachments
        from django.db.models import Sum

        if stock.storage:
            stock.storage.__dict__['attachments'] = list(stock.storage.attachments.all())
        if stock.lot:
            stock.lot.__dict__['attachments'] = list(stock.lot.attachments.all())
        if stock.part:
            stock.part.__dict__['attachments'] = list(stock.part.attachments.all())
            # Calculate total_stock
            total = Stock.objects.filter(
                part=stock.part,
                status__isnull=True
            ).aggregate(total=Sum('quantity'))['total'] or 0
            stock.part.total_stock = total

        return stock

    try:
        stock = await _update()
        return stock
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.delete("/stock/{stock_id}", status_code=204)
async def delete_stock(stock_id: UUID):
    """Delete a stock entry."""

    @sync_to_async
    def _delete():
        try:
            stock = Stock.objects.get(id=stock_id)
            stock.delete()
            return True
        except Stock.DoesNotExist:
            return False

    deleted = await _delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Stock entry not found")


# --- Lot Endpoints ---


def _get_lot_queryset():
    return Lot.objects.prefetch_related("attachments").select_related("order")


@router.get("/lots", response_model=List[LotSchema])
async def list_lots(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    @sync_to_async
    def _list():
        lots = list(_get_lot_queryset().all()[skip : skip + limit])
        # Eagerly convert attachments to lists
        for lot in lots:
            lot.__dict__['attachments'] = list(lot.attachments.all())
        return lots

    lots = await _list()
    return lots


@router.get("/lots/count", response_model=dict)
async def count_lots():
    count = await sync_to_async(_get_lot_queryset().count)()
    return {"count": count}


@router.get("/lots/{lot_id}", response_model=LotSchema)
async def get_lot(lot_id: UUID):
    @sync_to_async
    def _get():
        try:
            lot = _get_lot_queryset().get(id=lot_id)
            # Eagerly convert attachments to lists
            lot.__dict__['attachments'] = list(lot.attachments.all())
            return lot
        except Lot.DoesNotExist:
            return None

    lot = await _get()
    if lot is None:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot


@router.post("/lots", response_model=LotSchema, status_code=201)
async def create_lot(data: LotCreate):
    """Create a new lot/batch."""

    @sync_to_async
    def _create():
        lot_data = data.model_dump(exclude={"order_id"})

        # Validate order if provided
        order = None
        if data.order_id:
            try:
                order = Order.objects.get(id=data.order_id)
            except Order.DoesNotExist:
                raise ValueError("Order not found", 400)

        lot = Lot.objects.create(order=order, **lot_data)
        lot = _get_lot_queryset().get(id=lot.id)
        # Eagerly convert attachments to lists
        lot.__dict__['attachments'] = list(lot.attachments.all())
        return lot

    try:
        lot = await _create()
        return lot
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.put("/lots/{lot_id}", response_model=LotSchema)
async def update_lot(lot_id: UUID, data: LotUpdate):
    """Update a lot/batch."""

    @sync_to_async
    def _update():
        try:
            lot = Lot.objects.get(id=lot_id)
        except Lot.DoesNotExist:
            raise ValueError("Lot not found", 404)

        update_data = data.model_dump(exclude_unset=True)

        # Handle order foreign key
        if "order_id" in update_data:
            order_id = update_data.pop("order_id")
            if order_id is None:
                lot.order = None
            else:
                try:
                    lot.order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    raise ValueError("Order not found", 400)

        # Update remaining fields
        for field, value in update_data.items():
            setattr(lot, field, value)

        lot.save()
        lot = _get_lot_queryset().get(id=lot.id)
        # Eagerly convert attachments to lists
        lot.__dict__['attachments'] = list(lot.attachments.all())
        return lot

    try:
        lot = await _update()
        return lot
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.get("/low-stock", response_model=List[LowStockAlert])
async def get_low_stock_alerts():
    @sync_to_async
    def _get_low_stock():
        alerts = []
        parts = Part.objects.filter(low_stock_threshold__isnull=False).prefetch_related("stock_entries")
        for part in parts:
            total_stock = part.stock_entries.aggregate(total=Sum("quantity"))["total"] or 0
            if total_stock <= part.low_stock_threshold:
                status = "Critical" if total_stock <= (part.low_stock_threshold * 0.5) else "Warning"
                alerts.append(
                    LowStockAlert(
                        id=part.id,
                        name=part.name,
                        mpn=part.mpn or "",
                        stock=total_stock,
                        min=part.low_stock_threshold,
                        status=status,
                    )
                )
        return sorted(alerts, key=lambda x: x.stock)

    return await _get_low_stock()


@router.get("/occupancy", response_model=StorageOccupancySummary)
async def get_storage_occupancy():
    @sync_to_async
    def _get_occupancy():
        locations = list(Storage.objects.all())
        total_locations = len(locations)
        used_locations = 0
        location_quantities = []

        for location in locations:
            total_items = location.stock_in_location.aggregate(total=Sum("quantity", default=0))["total"] or 0
            if total_items > 0:
                used_locations += 1
            location_quantities.append((location.name, total_items))

        top_locations = sorted(location_quantities, key=lambda x: x[1], reverse=True)[:5]
        empty_locations = total_locations - used_locations
        used_percentage = round((used_locations / total_locations * 100), 1) if total_locations > 0 else 0

        return StorageOccupancySummary(
            total_locations=total_locations,
            used_locations=used_locations,
            empty_locations=empty_locations,
            used_percentage=used_percentage,
            top_locations=[StorageOccupancyItem(name=name, quantity=qty) for name, qty in top_locations],
        )

    return await _get_occupancy()
