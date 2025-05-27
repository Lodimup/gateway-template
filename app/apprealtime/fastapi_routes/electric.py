import httpx
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import StreamingResponse

from app.app_settings import APP_SETTINGS

router = APIRouter()


client = httpx.AsyncClient(timeout=25)

BASE_URL = "http://host.docker.internal:3000/v1/shape"  # this is the electric's url


@router.get("/shape-proxy/")
async def shape_proxy(request: Request):
    """
    Proxy endpoint for the Electric shape service.
    """
    # check header for Bearer token and get user_id, then modify the where clause to include AND user_id = $n-1, modify params[n-1] = <user_id>
    # Build the origin URL
    # Copy query params from incoming request
    params = dict(request.query_params)
    # Add source_id and secret if present
    if APP_SETTINGS.ELECTRIC_SOURCE_ID:
        params["source_id"] = APP_SETTINGS.ELECTRIC_SOURCE_ID
    if APP_SETTINGS.ELECTRIC_SOURCE_SECRET:
        params["secret"] = APP_SETTINGS.ELECTRIC_SOURCE_SECRET
    # Make the proxied request
    async with client.stream(
        "GET", APP_SETTINGS.ELECTRIC_URL, params=params, headers=request.headers
    ) as resp:
        # Remove problematic headers
        headers = dict(resp.headers)
        headers.pop("content-encoding", None)
        headers.pop("content-length", None)

        async def _task_close_response():
            await resp.aclose()

        # Stream the response body
        return StreamingResponse(
            iter([await resp.aread()]),
            status_code=resp.status_code,
            headers=headers,
            background=BackgroundTasks().add_task(_task_close_response),
        )
