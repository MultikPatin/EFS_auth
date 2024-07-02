from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter

from src.models.api.base import StringRepresent
from src.services.oauth2.google import OAuth2GoogleService, get_oauth2_google_service

router = APIRouter()


@router.get(
    "/oauth_google_login/",
    summary="Generate google oauth server authorization url and redirect there",
    dependencies=[Depends(RateLimiter(times=5, seconds=1))],
)
async def oauth_google_login(
    oauth2_service: OAuth2GoogleService = Depends(get_oauth2_google_service),
) -> RedirectResponse:
    """Endpoint to get to oauth server

    Generate google oauth server authorization url and redirect there

    Returns:
    - **RedirectResponse**: Redirect to google oauth server
    """
    authorization_url = await oauth2_service.get_google_authorization_url()
    return RedirectResponse(url=authorization_url)


@router.get(
    "/google_auth/",
    response_model=StringRepresent,
    summary="Get user info from oauth server and login",
    dependencies=[Depends(RateLimiter(times=5, seconds=1))],
)
async def google_auth(
    request: Request,
    oauth2_service: OAuth2GoogleService = Depends(get_oauth2_google_service),
) -> StringRepresent:
    """User authentication in the google auth service

    Get user info from google oauth server and login

    Returns:
    - **StringRepresent**: Status code with message "The google login was completed successfully"
    """
    await oauth2_service.login(
        request,
        await oauth2_service.checkin_oauth_user(
            await oauth2_service.auth_via_google(request)
        ),
    )
    return StringRepresent(
        code=HTTPStatus.OK,
        details="The google login was completed successfully",
    )
