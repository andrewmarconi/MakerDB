from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import socket
from inventory.schemas import StorageSchema
from django.conf import settings

router = APIRouter(prefix="/search", tags=["search"])


class SearchLocationsResponse(BaseModel):
    results: List[StorageSchema]
    count: int


def get_typesense_config():
    """Get Typesense configuration from Django settings."""
    try:
        socket.gethostbyname("typesense")
        host = "typesense"
    except socket.gaierror:
        host = "localhost"

    return {"url": f"http://{host}:8108", "api_key": settings.TYPESENSE_API_KEY}


async def typesense_request(method: str, path: str, body: Optional[dict] = None, query_params: Optional[dict] = None):
    """Make authenticated request to Typesense."""
    import httpx
    import logging

    logger = logging.getLogger(__name__)
    config = get_typesense_config()
    url = f"{config['url']}{path}"
    headers = {"X-TYPESENSE-API-KEY": config["api_key"]}

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=query_params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=body, params=query_params)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, params=query_params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Typesense HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Typesense error: {e.response.text}")


@router.get("/locations", response_model=SearchLocationsResponse)
async def search_locations(
    q: str,
    skip: int = 0,
    limit: int = 100,
    has_stock: Optional[bool] = None,
    tags: Optional[str] = None,
):
    """
    Search storage locations via Typesense with filters.
    Returns full Storage objects from Django after Typesense search.
    """
    from asgiref.sync import sync_to_async
    from inventory.models import Storage, Stock
    from django.db.models import Exists, OuterRef
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Search via Typesense
        params = {
            "q": q,
            "query_by": "name,description",
            "limit": 250,  # Typesense max per page
            "infix": "always",  # Enable substring matching
        }

        results = await typesense_request("GET", "/collections/storage/documents/search", query_params=params)

        # Extract matching IDs
        matching_ids = [hit["document"]["id"] for hit in results.get("hits", [])]

        if not matching_ids:
            return {"results": [], "count": 0}

        # Fetch full Storage objects from Django with filters
        @sync_to_async
        def _get_filtered_locations():
            queryset = Storage.objects.filter(id__in=matching_ids).prefetch_related("attachments")

            # Apply filters
            if has_stock is not None:
                if has_stock:
                    queryset = queryset.filter(stock_in_location__quantity__gt=0).distinct()
                else:
                    has_stock_subquery = Stock.objects.filter(storage_id=OuterRef("pk"), quantity__gt=0)
                    queryset = queryset.exclude(Exists(has_stock_subquery))

            if tags:
                tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                for tag in tag_list:
                    queryset = queryset.filter(tags__contains=[tag])

            # Order by Typesense relevance (maintain ID order from Typesense)
            id_order = {id: index for index, id in enumerate(matching_ids)}
            locations = list(queryset)
            locations.sort(key=lambda loc: id_order.get(str(loc.id), 999999))

            # Eagerly convert attachments to lists
            for location in locations:
                location.__dict__['attachments'] = list(location.attachments.all())

            # Apply pagination
            total_count = len(locations)
            paginated = locations[skip : skip + limit]

            return {"results": paginated, "count": total_count}

        return await _get_filtered_locations()

    except Exception as e:
        logger.error(f"Error in search_locations: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/suggestions")
async def location_suggestions(q: str, limit: int = 5):
    """Get autocomplete suggestions for locations."""
    try:
        results = await typesense_request(
            "GET",
            "/collections/storage/documents/search",
            query_params={
                "q": q,
                "query_by": "name",
                "limit": limit,
                "infix": "always",
                "drop_tokens_threshold": 0,
            },
        )
        suggestions = [hit["document"]["name"] for hit in results.get("hits", [])]
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
