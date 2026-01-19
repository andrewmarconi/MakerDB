from typing import List
from fastapi import APIRouter, HTTPException
from uuid import UUID
from procurement.models import Order, Offer
from procurement.schemas import OrderSchema, OfferSchema
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/procurement", tags=["Procurement"])

@router.get("/orders", response_model=List[OrderSchema])
async def list_orders():
    orders = await sync_to_async(list)(Order.objects.select_related('vendor').prefetch_related('attachments').all())
    return orders

@router.get("/orders/{order_id}", response_model=OrderSchema)
async def get_order(order_id: UUID):
    try:
        order = await sync_to_async(Order.objects.select_related('vendor').prefetch_related('attachments').get)(id=order_id)
        return order
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")

@router.get("/offers", response_model=List[OfferSchema])
async def list_offers():
    offers = await sync_to_async(list)(Offer.objects.select_related('vendor', 'part').prefetch_related('attachments').all())
    return offers
