# pylint: skip-file
import os
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, Client, ConnectError, ReadError, Response

from .data_generating_testing import (
    generate_random_keycloak_token,
    generate_test_credentials,
)

load_dotenv()

AUTH_BACKEND_PORT = os.getenv("AUTH_BACKEND_PORT")
REACT_APP_BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL")
REACT_APP_DOMAIN_NAME = os.getenv("REACT_APP_DOMAIN_NAME")
KEYCLOAK_ADMIN = os.getenv("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
KC_PORT = os.getenv("KC_PORT")
QUIZ_BACKEND_PORT = os.getenv("QUIZ_BACKEND_PORT")
KEYDB_PORT = os.getenv("KEYDB_PORT")

USER, PASSWORD = generate_test_credentials()
ACCESS_TOKEN = generate_random_keycloak_token()
REFRESH_TOKEN = generate_random_keycloak_token()
BASE_URL = f"{REACT_APP_BACKEND_URL}{REACT_APP_DOMAIN_NAME}"
TOKEN_URL = f"{BASE_URL}/api/v1/auth"

os.environ["TESTING"] = "true"


class MockKeycloakOpenID:
    """
    A mock class for testing Keycloak OpenID authentication.

    This class provides a mock implementation of the Keycloak OpenID
    client for use in asynchronous tests. It allows for the simulation
    of authentication flows without requiring a real Keycloak server.

    Attributes:
        base_url (str): The base URL for the mock Keycloak server.
    """

    def __init__(self, base_url: str):
        """
        Initializes the MockKeycloakOpenID with a base URL.

        Args:
            base_url (str): The base URL of the Keycloak server.
        """
        self.base_url = base_url

    @classmethod
    async def fetch_token(cls, username: str, password: str) -> Response:
        """
        Mocks the token response for user authentication.

        This method simulates a successful token response when valid
        credentials are provided.

        :param str username: The username for authentication.
        :param str password: The password for authentication.
        :return: A mocked Response object containing the access token.
        """
        if username == USER and password == PASSWORD:
            return Response(
                status_code=status.HTTP_200_OK,
                json={
                    "access_token": ACCESS_TOKEN,
                    "refresh_token": REFRESH_TOKEN,
                    "token_type": "bearer",
                },
            )
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            json={
                "error": "invalid_credentials",
                "access_token": "",
                "refresh_token": "",
            },
        )

    @classmethod
    async def refresh_token(
        cls,
        token: str,
    ) -> Response:
        """
        Mocks the token response for user authentication.

        This method simulates a successful token response when valid
        credentials are provided.

        :param str username: The username for authentication.
        :param str password: The password for authentication.
        :return: A mocked Response object containing the access token.
        """
        if token == ACCESS_TOKEN:
            return Response(
                status_code=status.HTTP_200_OK,
                json={
                    "access_token": ACCESS_TOKEN,
                    "refresh_token": REFRESH_TOKEN,
                    "token_type": "bearer",
                },
            )
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, json={"error": "token"}
        )

    @classmethod
    def create_event(cls, token: str):
        """
        Simulates events creation

        :param str token: The access token for user information retrieval.

        :returns dict: A dictionary containing mock user information.
        :raises Exception: If the token is invalid.
        """
        if token == ACCESS_TOKEN:
            return Response(
                status_code=status.HTTP_200_OK,
                json={
                    "name": "string",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "client_info": "admin-cli",
                },
            )
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            json={"error": "invalid_credentials"},
        )


@pytest.fixture
async def client_mock_keycloak():
    """
    Fixture that provides AsyncClient for testing with mock Keycloak container

    This fixture initializes AsyncClient before the test and ensures
    that it is properly finished after the test is completed

    :return: The instance of AsyncClient configured for testing
    """
    # Base URL for the mock Keycloak container
    base_url = BASE_URL
    # Create an instance of the mock Keycloak client
    mock_keycloak = MockKeycloakOpenID(base_url)
    # Create an AsyncClient for making requests
    async with AsyncClient(base_url=base_url) as client:
        # Patch the methods of the mock Keycloak client
        with (
            patch.object(
                mock_keycloak, "fetch_token", new_callable=AsyncMock
            ) as mock_fetch_token,
            patch.object(
                mock_keycloak, "refresh_token", new_callable=AsyncMock
            ) as mock_refresh_token,
            patch.object(
                mock_keycloak, "create_event", new_callable=AsyncMock
            ) as mock_create_event,
        ):
            mock_fetch_token.config = "mocked_config"
            # Set return values for the mocked methods
            mock_fetch_token.return_value = {
                "access_token": ACCESS_TOKEN,
                "refresh_token": REFRESH_TOKEN,
                "expires_in": 60,
                "refresh_expires_in": 1800,
                "not_before_policy": "0",
            }
            mock_refresh_token.config = "mocked_config"
            mock_refresh_token.return_value = {
                "access_token": generate_random_keycloak_token(),
                "refresh_token": generate_random_keycloak_token(),
                "expires_in": 60,
                "refresh_expires_in": 1800,
                "not_before_policy": "0",
            }
            mock_create_event.config = "mocked_config"
            mock_create_event.return_value = {
                "name": "string",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "client_info": "admin-cli",
            }

            yield client, mock_keycloak


def is_responsive(url) -> bool:
    """
    Check if the input URL is responsive

    :param str url: The URL for responsiveness check

    :return bool: True if the response status code is successful, False otherwise
    """
    try:
        with Client() as client:
            response = client.get(url=url)
            if response.status_code in {status.HTTP_200_OK, status.HTTP_302_FOUND}:
                return True
    except (ConnectError, ReadError):
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """
    Fixture that provides the path to the Docker Compose file

    :param pytestconfig pytestconfig: The pytest configuration object

    :return Path: The path to the Docker Compose file
    """
    return Path(pytestconfig.rootdir).parent / "compose.yaml"


@pytest.fixture(scope="function")
async def backend_container_quiz_runner(docker_ip, docker_services):
    """
    Fixture that ensures the backend quiz container is up and responsive

    This fixture waits until the HTTP service is responsive and yields
    AsyncClient instance for making requests to the service

    :param str docker_ip: The IP address of the Docker service
    :param docker_services docker_services: The Docker services fixture

    :yield AsyncClient: An AsyncClient instance for the backend service
    """
    try:
        AUTH_BACKEND_PORT_VALUE = int(AUTH_BACKEND_PORT)
    except ValueError as excp:
        raise ValueError("Converting value to integer error") from excp

    try:
        KC_PORT_VALUE = int(KC_PORT)
    except ValueError as excp:
        raise ValueError("Converting value to integer error") from excp

    try:
        QUIZ_BACKEND_PORT_VALUE = int(QUIZ_BACKEND_PORT)
    except ValueError as excp:
        raise ValueError("Converting value to integer error") from excp

    port_backend = docker_services.port_for("auth-backend", AUTH_BACKEND_PORT_VALUE)
    url_auth_backend = f"http://{docker_ip}:{port_backend}/check-auth"
    port_keycloak = docker_services.port_for("keycloak", KC_PORT_VALUE)
    url_keycloak = f"http://{docker_ip}:{port_keycloak}"
    port_quiz_backend = docker_services.port_for(
        "quiz-backend-api", QUIZ_BACKEND_PORT_VALUE
    )
    url_quiz_backend = f"http://{docker_ip}:{port_quiz_backend}/check-game"
    docker_services.wait_until_responsive(
        timeout=410, pause=3, check=lambda: is_responsive(url=url_auth_backend)
    )
    docker_services.wait_until_responsive(
        timeout=410, pause=5, check=lambda: is_responsive(url=url_keycloak)
    )
    docker_services.wait_until_responsive(
        timeout=410, pause=1, check=lambda: is_responsive(url=url_quiz_backend)
    )
    url_auth_backend = url_auth_backend.replace("/check-auth", "")
    url_quiz_backend = url_quiz_backend.replace("/check-game", "")
    async with (
        AsyncClient(base_url=url_auth_backend) as async_auth_client,
        AsyncClient(base_url=url_quiz_backend) as async_quiz_client,
    ):
        time.sleep(3)
        yield {"auth_backend": async_auth_client, "quiz_backend": async_quiz_client}


@pytest.fixture(scope="function")
async def admin_user_tokens(backend_container_quiz_runner) -> dict[str, str]:
    """
    Fixture that provides admin users access tokens for Keycloak container

    :return dict[str, str]: Access tokens
    """
    async_auth_client = backend_container_quiz_runner["auth_backend"]
    response = await async_auth_client.post(
        "/api-auth/v1/auth/token",
        data={"username": KEYCLOAK_ADMIN, "password": KEYCLOAK_ADMIN_PASSWORD},
    )
    access_token = response.json()["access_token"]
    response_token_introspection = await async_auth_client.post(
        "/api-auth/v1/auth/introspect",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return {
        "access_token": access_token,
        "refresh_token": response.json()["refresh_token"],
        "user_sub_id": response_token_introspection.json()["sub"],
    }


@pytest.fixture(scope="function")
async def common_user_tokens(backend_container_quiz_runner) -> dict[str, str]:
    """
    Fixture that provides common users access tokens for Keycloak container

    :return dict[str, str]: Access tokens
    """
    async_auth_client = backend_container_quiz_runner["auth_backend"]
    await async_auth_client.post(
        "/api-auth/v1/auth/register",
        data={"username": USER, "password": PASSWORD},
    )
    response = await async_auth_client.post(
        "/api-auth/v1/auth/token",
        data={"username": USER, "password": PASSWORD},
    )
    access_token = response.json()["access_token"]
    response_token_introspection = await async_auth_client.post(
        "/api-auth/v1/auth/introspect",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return {
        "access_token": access_token,
        "refresh_token": response.json()["refresh_token"],
        "user_sub_id": response_token_introspection.json()["sub"],
    }
