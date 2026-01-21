from typing import List
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
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
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# --- Storage Location Endpoints ---


def _get_storage_queryset():
    return Storage.objects.prefetch_related("attachments")


@router.get("/locations", response_model=List[StorageSchema])
async def list_locations(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    locations = await sync_to_async(list)(_get_storage_queryset().all()[skip : skip + limit])
    return locations


@router.get("/locations/count", response_model=dict)
async def count_locations():
    count = await sync_to_async(_get_storage_queryset().count)()
    return {"count": count}


@router.get("/locations/{location_id}", response_model=StorageSchema)
async def get_location(location_id: UUID):
    try:
        location = await sync_to_async(_get_storage_queryset().get)(id=location_id)
        return location
    except Storage.DoesNotExist:
        raise HTTPException(status_code=404, detail="Storage location not found")


@router.post("/locations", response_model=StorageSchema, status_code=201)
async def create_location(data: StorageCreate):
    """Create a new storage location."""

    @sync_to_async
    def _create():
        location = Storage.objects.create(**data.model_dump())
        return _get_storage_queryset().get(id=location.id)

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
    return Stock.objects.select_related("part", "storage", "lot").prefetch_related(
        "storage__attachments", "lot__attachments"
    )


@router.get("/stock", response_model=List[StockSchema])
async def list_stock(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    stock = await sync_to_async(list)(_get_stock_queryset().all()[skip : skip + limit])
    return stock


@router.get("/stock/count", response_model=dict)
async def count_stock():
    count = await sync_to_async(_get_stock_queryset().count)()
    return {"count": count}


@router.get("/stock/{stock_id}", response_model=StockSchema)
async def get_stock(stock_id: UUID):
    try:
        stock = await sync_to_async(_get_stock_queryset().get)(id=stock_id)
        return stock
    except Stock.DoesNotExist:
        raise HTTPException(status_code=404, detail="Stock entry not found")


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

        stock_data = data.model_dump(exclude={"part_id", "storage_id", "lot_id"})
        stock = Stock.objects.create(part=part, storage=storage, lot=lot, **stock_data)
        return _get_stock_queryset().get(id=stock.id)

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
        return _get_stock_queryset().get(id=stock.id)

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
    lots = await sync_to_async(list)(_get_lot_queryset().all()[skip : skip + limit])
    return lots


@router.get("/lots/count", response_model=dict)
async def count_lots():
    count = await sync_to_async(_get_lot_queryset().count)()
    return {"count": count}


@router.get("/lots/{lot_id}", response_model=LotSchema)
async def get_lot(lot_id: UUID):
    try:
        lot = await sync_to_async(_get_lot_queryset().get)(id=lot_id)
        return lot
    except Lot.DoesNotExist:
        raise HTTPException(status_code=404, detail="Lot not found")


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
        return _get_lot_queryset().get(id=lot.id)

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
        return _get_lot_queryset().get(id=lot.id)

    try:
        lot = await _update()
        return lot
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])
