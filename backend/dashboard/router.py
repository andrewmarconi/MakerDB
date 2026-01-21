from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class DashboardStats(BaseModel):
    inventoryValue: float
    currency: str = "USD"
    valueTrends: List[int] = [0, 0, 0, 0, 0, 0, 0]


class DashboardSummary(BaseModel):
    totalParts: int
    openOrders: int
    activeProjects: int


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    @sync_to_async
    def _get_summary():
        from parts.models import Part
        from procurement.models import Order
        from projects.models import Project

        total_parts = Part.objects.count()
        open_orders = Order.objects.filter(status="open").count()
        active_projects = Project.objects.filter(status="active").count()

        return DashboardSummary(totalParts=total_parts, openOrders=open_orders, activeProjects=active_projects)

    return await _get_summary()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    @sync_to_async
    def _get_stats():
        from django.db.models import Sum
        from inventory.models import Stock

        total_value = Stock.objects.aggregate(total=Sum("quantity") * Sum("price_unit"))["total"] or 0

        value_trends = [0, 0, 0, 0, 0, 0, 0]

        return DashboardStats(inventoryValue=float(total_value), currency="USD", valueTrends=value_trends)

    return await _get_stats()
