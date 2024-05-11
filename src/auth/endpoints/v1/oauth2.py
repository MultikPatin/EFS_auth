from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response

from src.auth.models.api.base import StringRepresent
from src.auth.services.oauth2 import OAuth2Service, get_oauth2_service

router = APIRouter()


@router.get(
    "/oauth_login/",
    summary="Generate oauth server authorization url and redirect there",
)
async def oauth_login(
    oauth2_service: OAuth2Service = Depends(get_oauth2_service),
) -> RedirectResponse:
    """Endpoint to get to oauth server

    Generate oauth server authorization url and redirect there

    Returns:
    - **RedirectResponse**: Redirect to oauth server
    """
    authorization_url = await oauth2_service.get_authorization_url()
    return RedirectResponse(url=authorization_url)


@router.get(
    "/auth/",
    response_model=StringRepresent,
    summary="Get user info from oauth server and login",
)
async def auth(
    request: Request,
    response: Response,
    oauth2_service: OAuth2Service = Depends(get_oauth2_service),
) -> StringRepresent:
    """User authentication in the Auth service

    Get user info from oauth server and login

    Returns:
    - **StringRepresent**: Status code with message "The login was completed successfully"
    """
    result = await oauth2_service.auth_via_google(request, response)
    if isinstance(result, dict):
        user_data = await oauth2_service.checkin_oauth_user(result)
    else:
        user_data = result
    await oauth2_service.login(request, user_data)
    return StringRepresent(
        code=HTTPStatus.OK, details="The login was completed successfully"
    )
