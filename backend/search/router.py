from fastapi import APIRouter, HTTPException
from typing import Optional
import os
import socket

router = APIRouter(prefix="/search", tags=["search"])

try:
    socket.gethostbyname("typesense")
    TYPESENSE_HOST = "typesense"
except socket.gaierror:
    TYPESENSE_HOST = "localhost"

TYPESENSE_URL = f"http://{TYPESENSE_HOST}:8108"
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY", "secret")


async def typesense_request(method: str, path: str, body: Optional[dict] = None, query_params: Optional[dict] = None):
    """Make authenticated request to Typesense."""
    import httpx

    url = f"{TYPESENSE_URL}{path}"
    headers = {"X-TYPESENSE-API-KEY": TYPESENSE_API_KEY}

    async with httpx.AsyncClient() as client:
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


@router.get("/locations")
async def search_locations(q: str, limit: int = 10, filter_by: Optional[str] = None):
    """Search storage locations via Typesense."""
    try:
        params = {
            "q": q,
            "query_by": "name,description",
            "limit": limit,
        }
        if filter_by:
            params["filter_by"] = filter_by

        results = await typesense_request("GET", "/collections/storage/documents/search", query_params=params)
        return {"hits": results.get("hits", [])}
    except Exception as e:
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
                "prefix": "true",
                "drop_tokens_threshold": 0,
            },
        )
        suggestions = [hit["document"]["name"] for hit in results.get("hits", [])]
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
