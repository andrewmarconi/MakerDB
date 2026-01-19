from typing import List
from fastapi import APIRouter, HTTPException
from uuid import UUID
from inventory.models import Storage, Lot, Stock
from inventory.schemas import StorageSchema, LotSchema, StockSchema
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/locations", response_model=List[StorageSchema])
async def list_locations():
    locations = await sync_to_async(list)(Storage.objects.prefetch_related('attachments').all())
    return locations

@router.get("/stock", response_model=List[StockSchema])
async def list_stock():
    stock = await sync_to_async(list)(Stock.objects.select_related('part', 'storage', 'lot').all())
    return stock

@router.get("/lots", response_model=List[LotSchema])
async def list_lots():
    lots = await sync_to_async(list)(Lot.objects.prefetch_related('attachments').all())
    return lots
