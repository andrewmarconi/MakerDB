from typing import List
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from core.models import Company
from core.schemas import CompanySchema, CompanyCreate
from asgiref.sync import sync_to_async

router = APIRouter(tags=["Core"])


@router.get("/companies", response_model=List[CompanySchema])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_manufacturer: bool = None,
    is_vendor: bool = None,
):
    """List companies with optional filtering."""

    @sync_to_async
    def _list():
        queryset = Company.objects.all()
        if is_manufacturer is not None:
            queryset = queryset.filter(is_manufacturer=is_manufacturer)
        if is_vendor is not None:
            queryset = queryset.filter(is_vendor=is_vendor)
        return list(queryset[skip : skip + limit])

    companies = await _list()
    return companies


@router.get("/companies/count", response_model=dict)
async def count_companies(is_manufacturer: bool = None, is_vendor: bool = None):
    @sync_to_async
    def _count():
        queryset = Company.objects.all()
        if is_manufacturer is not None:
            queryset = queryset.filter(is_manufacturer=is_manufacturer)
        if is_vendor is not None:
            queryset = queryset.filter(is_vendor=is_vendor)
        return queryset.count()

    count = await _count()
    return {"count": count}


@router.get("/companies/{company_id}", response_model=CompanySchema)
async def get_company(company_id: UUID):
    """Get a company by ID."""
    try:
        company = await sync_to_async(Company.objects.get)(id=company_id)
        return company
    except Company.DoesNotExist:
        raise HTTPException(status_code=404, detail="Company not found")


@router.post("/companies", response_model=CompanySchema, status_code=201)
async def create_company(data: CompanyCreate):
    """Create a new company (manufacturer or vendor)."""

    @sync_to_async
    def _create():
        company = Company.objects.create(**data.model_dump())
        return Company.objects.get(id=company.id)

    try:
        company = await _create()
        return company
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/companies/{company_id}", response_model=CompanySchema)
async def update_company(company_id: UUID, data: CompanyCreate):
    """Update a company."""

    @sync_to_async
    def _update():
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise ValueError("Company not found", 404)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company, field, value)

        company.save()
        return Company.objects.get(id=company.id)

    try:
        company = await _update()
        return company
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.delete("/companies/{company_id}", status_code=204)
async def delete_company(company_id: UUID):
    """Delete a company."""

    @sync_to_async
    def _delete():
        try:
            company = Company.objects.get(id=company_id)
            company.delete()
            return True
        except Company.DoesNotExist:
            return False

    deleted = await _delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
