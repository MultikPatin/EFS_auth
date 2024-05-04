from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.services.oauth2 import OAuth2Service, get_oauth2_service

router = APIRouter()


@router.get("/login/", summary="Issuing a JWT token")
async def login(
    request: Request,
    oauth2_service: OAuth2Service = Depends(get_oauth2_service),
) -> RedirectResponse:
    authorization_url = await oauth2_service.get_authorization_url(request)
    return RedirectResponse(url=authorization_url)


@router.get("/auth/", summary="Issuing a JWT token")
async def auth(
    request: Request,
    oauth2_service: OAuth2Service = Depends(get_oauth2_service),
):
    await oauth2_service.auth_via_google(request)
    return RedirectResponse(url="/auth/v1/oauth2/logout/")


@router.get("/logout/", summary="Logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/auth/v1/oauth2/")
