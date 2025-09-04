import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repository.game import CRUDGame

load_dotenv()

game_crud = CRUDGame()

AUTH_BACKEND_DOMAIN = (
    f"{os.getenv('REACT_APP_BACKEND_URL')}{os.getenv('REACT_APP_DOMAIN_NAME')}"
)

if os.getenv("REACT_APP_NODE_MODE") != "production":
    AUTH_BACKEND_DOMAIN = (
        f"{os.getenv('REACT_APP_BACKEND_URL')}{os.getenv('REACT_APP_DOMAIN_NAME')}"
    )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{AUTH_BACKEND_DOMAIN}/api-auth/v1/auth/token"
)


def verify_permission(required_roles: list):
    """
    Verify user permissions based on required roles.

    This function returns an asynchronous dependency that verifies if the user
    associated with the provided token has the required roles to perform a specific action.
    If the user does not have the required roles, an HTTP 403 Forbidden error is raised.
    If the token is invalid or cannot be decoded, an HTTP 401 Unauthorized error is raised.

    :param list required_roles: A list of roles that are required to perform the action.
    If no roles are provided, an empty list is used

    :return dict[str, str]: A dictionary containing the decoded token information if the user has
             the required roles.
    """
    if not required_roles:
        required_roles = []

    async def verify_permission_token(  # pylint: disable=W0612
        token: str = Depends(oauth2_scheme),
    ) -> dict[str, str]:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient() as client:
                token_info_response = await client.post(
                    f"{AUTH_BACKEND_DOMAIN}/api-auth/v1/auth/verify-token",
                    headers=headers,
                )

                token_info_response.raise_for_status()  # Raises an error for 4xx/5xx responses

                token_info = token_info_response.json()  # Parse the JSON response
                user_groups = token_info.get("groups", [])
                for role in required_roles:
                    if role not in user_groups:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Role '{role}' is required to perform this action",
                        )

                return token_info_response
        except Exception as exception:
            if (
                exception
                and hasattr(exception, "status_code")
                and hasattr(exception, "detail")
            ):
                raise HTTPException(
                    status_code=exception.status_code,
                    detail=exception.detail,
                ) from exception
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{str(exception)} - {exception.__class__}",
            ) from exception

    return verify_permission_token  # Return the inner function


async def verify_token(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    """
    Verify the provided token.

    This function checks the validity of the token by sending a request to the
    authentication backend. If the token is valid, it returns the token information.
    If the token is invalid, an HTTP 401 Unauthorized error is raised

    :param str token: The token to be verified

    :returns dict[str, str] token_info_response: Dictionary containing the token information
    if the token is valid
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            token_info_response = await client.post(
                f"{AUTH_BACKEND_DOMAIN}/api-auth/v1/auth/verify-token", headers=headers
            )

            token_info_response.raise_for_status()  # Raises an error for 4xx/5xx responses

        return token_info_response
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(exception)} - {exception.__class__}",
        ) from exception


async def create_game(db: AsyncSession, game_data: dict):
    """
    Create new game entry in the database.

    This function takes the game data and creates a new game record in the database.

    :param AsyncSession db: The database session to use for the operation
    :param dict game_data: A dictionary containing the data for the new game

    :returns: The created game record.
    :rtype: Any
    """
    return await game_crud.create(db=db, game_data=game_data)


async def update_game_result(db: AsyncSession, game_id: int, game_data: dict[str, Any]):
    """
    Update the result of an existing game.

    This function updates the game result for a specific game identified by its ID.

    :param db: The database session to use for the operation.
    :type db: AsyncSession

    :param game_id: The ID of the game to update
    :type game_id: int

    :param dict[str, Any] game_data: A dictionary containing the updated game data

    :returns Any: The updated game record
    """
    return await game_crud.update_game_result(
        db=db, game_id=game_id, game_data=game_data
    )


async def fetch_games(db: AsyncSession):
    """
    Fetching all games from the database.
    The function retrieves all game records from the database

    :param AsyncSession db: The database session to use for the operation

    :returns Any: List of all game records
    """
    return await game_crud.get_all_games(db=db)
