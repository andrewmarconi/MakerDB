from typing import List
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from procurement.models import Order, Offer
from procurement.schemas import OrderSchema, OfferSchema
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.get("/orders", response_model=List[OrderSchema])
async def list_orders(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    orders = await sync_to_async(list)(
        Order.objects.select_related("vendor").prefetch_related("attachments").all()[skip : skip + limit]
    )
    return orders


@router.get("/orders/count", response_model=dict)
async def count_orders():
    count = await sync_to_async(Order.objects.count)()
    return {"count": count}


@router.get("/orders/{order_id}", response_model=OrderSchema)
async def get_order(order_id: UUID):
    try:
        order = await sync_to_async(Order.objects.select_related("vendor").prefetch_related("attachments").get)(
            id=order_id
        )
        return order
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")


@router.get("/offers", response_model=List[OfferSchema])
async def list_offers(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    offers = await sync_to_async(list)(
        Offer.objects.select_related("vendor", "part").prefetch_related("attachments").all()[skip : skip + limit]
    )
    return offers


@router.get("/offers/count", response_model=dict)
async def count_offers():
    count = await sync_to_async(Offer.objects.count)()
    return {"count": count}
