from fastapi import APIRouter, HTTPException
import httpx
from app.config.services_config import USER_SERVICE_URL

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def test():
    return {"message": "User proxy works"}