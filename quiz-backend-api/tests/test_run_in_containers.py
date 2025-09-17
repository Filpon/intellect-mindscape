import json
import random
from datetime import datetime, timezone

import pytest
from fastapi import status


@pytest.mark.anyio
async def test_health_check(backend_container_quiz_runner):
    """
    Testing the health check endpoint.

    The test verifies that the health check can be performed by sending
    GET request to the `/check-game` endpoint. It checks that the response
    status code is 200 OK

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    response = await async_quiz_client.get(url="/check-game")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_admin_user_create_game_result(
    backend_container_quiz_runner, admin_user_tokens
):
    """
    Testing the creation of a game result.

    The test verifies that a game result can be successfully created
    by sending POST request to the `/api/v1/games/create` endpoint
    with a valid game request payload. It checks that the response
    status code is 200 OK and that the response contains an ID

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param admin_user_tokens: Dictionary containing the access token and refresh token
        for admin user, used for authentication in the request
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    latency_seconds_list = [21, 90, 180]

    game_request = {
        "user_sub_id": admin_user_tokens["user_sub_id"],
        "latency_seconds": random.choice(latency_seconds_list),
        "mode": random.choice(modes_list),
    }
    response = await async_quiz_client.post(
        url="/api/v1/games/create",
        headers={"Authorization": f"Bearer {admin_user_tokens['access_token']}"},
        json=game_request,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_common_user_create_game_result(
    backend_container_quiz_runner, common_user_tokens
):
    """
    Testing the creation of a game result.

    The test verifies that a game result can be successfully created
    by sending a POST request to the `/api/v1/games/create` endpoint
    with a valid game request payload. It checks that the response
    status code is 200 OK and that the response contains an ID

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param common_user_tokens: Fixture that provides the token and refresh token
        for common user
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    latency_seconds_list = [21, 90, 180]

    game_request = {
        "user_sub_id": common_user_tokens["user_sub_id"],
        "latency_seconds": random.choice(latency_seconds_list),
        "mode": random.choice(modes_list),
    }
    response = await async_quiz_client.post(
        url="/api/v1/games/create",
        headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
        json=game_request,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_admin_user_submit_game_result(
    backend_container_quiz_runner, admin_user_tokens
):
    """
    Testing submitting game result.

    The test verifies that game result can be successfully submitted
    by sending PATCH request to the `/api/v1/games/results` endpoint
    with a valid game result payload. It checks that the response
    status code is 200 OK

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param admin_user_tokens: Dictionary containing the access token and refresh token
        for admin user, used for authentication in the request
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    latency_seconds_list = [21, 90, 180]

    game_request = {
        "user_sub_id": admin_user_tokens["user_sub_id"],
        "latency_seconds": random.choice(latency_seconds_list),
        "mode": random.choice(modes_list),
    }
    response_creation = await async_quiz_client.post(
        url="/api/v1/games/create",
        headers={"Authorization": f"Bearer {admin_user_tokens['access_token']}"},
        json=game_request,
    )
    assert response_creation.status_code == status.HTTP_200_OK

    correct_score = random.randint(5, 20)
    incorrect_score = random.randint(5, 20)
    total_score = correct_score + incorrect_score
    game_result = {
        "id": json.loads(response_creation.text)["id"],
        "status": "completed",
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "correct_score": correct_score,
        "incorrect_score": incorrect_score,
        "total_score": total_score,
    }
    response = await async_quiz_client.patch(
        url="/api/v1/games/results",
        headers={"Authorization": f"Bearer {admin_user_tokens['access_token']}"},
        json=game_result,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_common_user_submit_game_result(
    backend_container_quiz_runner, common_user_tokens
):
    """
    Testing submitting game result.

    The test verifies that game result can be successfully submitted
    by sending PATCH request to the `/api/v1/games/results` endpoint
    with a valid game result payload. It checks that the response
    status code is 200 OK

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param common_user_tokens: Fixture that provides the token and refresh token
        for common user
    """

    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    latency_seconds_list = [21, 90, 180]

    game_request = {
        "user_sub_id": common_user_tokens["user_sub_id"],
        "latency_seconds": random.choice(latency_seconds_list),
        "mode": random.choice(modes_list),
    }
    response_creation = await async_quiz_client.post(
        url="/api/v1/games/create",
        headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
        json=game_request,
    )
    assert response_creation.status_code == status.HTTP_200_OK

    correct_score = random.randint(5, 20)
    incorrect_score = random.randint(5, 20)
    total_score = correct_score + incorrect_score

    game_result = {
        "id": json.loads(response_creation.text)["id"],
        "status": "completed",
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "correct_score": correct_score,
        "incorrect_score": incorrect_score,
        "total_score": total_score,
    }
    response = await async_quiz_client.patch(
        url="/api/v1/games/results",
        headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
        json=game_result,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_translations(backend_container_quiz_runner):
    """
    Testing retrieving translations for a specified language.

    The test verifies that translations can be fetched by sending
    GET request to the `/api/v1/translations/{language}` endpoint.
    It checks that the response status code is 200 OK and that the
    response is a dictionary

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    languages_list = [
        "ru",
        "en",
    ]
    language = random.choice(languages_list)
    response = await async_quiz_client.get(f"/api/v1/translations/{language}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)


@pytest.mark.anyio
async def test_fetch_all_admin_user_stats(
    backend_container_quiz_runner, admin_user_tokens
):
    """
    Testing fetching all user data based on user subscription ID.

    The test verifies that all user-related data can be fetched
    by sending a GET request to the `/api/v1/stats/all/{user_sub_id}`
    endpoint. It checks that the response status code is 200 OK
    and that the response is a list

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param admin_user_tokens: Dictionary containing the access token and refresh token
        for admin user, used for authentication in the request
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    user_sub_id = admin_user_tokens["user_sub_id"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    latency_seconds_list = [21, 90, 180]

    correct_score = random.randint(5, 20)
    incorrect_score = random.randint(5, 20)
    total_score = correct_score + incorrect_score

    creation_counter_numbers = random.randint(1, 5)

    for _ in range(creation_counter_numbers):
        game_request = {
            "user_sub_id": user_sub_id,
            "latency_seconds": random.choice(latency_seconds_list),
            "mode": random.choice(modes_list),
            "status": "completed",
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "correct_score": correct_score,
            "incorrect_score": incorrect_score,
            "total_score": total_score,
        }
        response_creation = await async_quiz_client.post(
            url="/api/v1/games/create",
            headers={"Authorization": f"Bearer {admin_user_tokens['access_token']}"},
            json=game_request,
        )
        assert response_creation.status_code == status.HTTP_200_OK

    response = await async_quiz_client.get(
        url=f"/api/v1/stats/all/{user_sub_id}",
        headers={"Authorization": f"Bearer {admin_user_tokens['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_fetch_all_common_user_stats(
    backend_container_quiz_runner, common_user_tokens
):
    """
    Testing fetching all user data based on user subscription ID.

    This test verifies that all user-related data can be fetched
    by sending GET request to the `/api/v1/stats/all/{user_sub_id}`
    endpoint. It checks that the response status code is 200 OK
    and that the response is a list

    :param backend_container_quiz_runner: Fixture that provides way to
        run the backend quiz container and interact with it during tests
    :param common_user_tokens: Fixture that provides the token and refresh token
        for common user
    """
    async_quiz_client = backend_container_quiz_runner["quiz_backend"]
    user_sub_id = common_user_tokens["user_sub_id"]
    modes_list = ["music", "arithmetic", "trigonometry"]
    modes_incorrect_score = {"music": 0, "arithmetic": 0, "trigonometry": 0}
    modes_correct_score = {"music": 0, "arithmetic": 0, "trigonometry": 0}
    latency_seconds_list = [21, 90, 180]
    creation_counter_numbers = random.randint(1, 5)

    for _ in range(creation_counter_numbers):
        correct_score = random.randint(5, 20)
        incorrect_score = random.randint(5, 20)
        total_score = correct_score + incorrect_score
        mode = random.choice(modes_list)
        game_request = {
            "user_sub_id": user_sub_id,
            "latency_seconds": random.choice(latency_seconds_list),
            "mode": mode,
            "status": "completed",
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "correct_score": correct_score,
            "incorrect_score": incorrect_score,
            "total_score": total_score,
        }
        response_creation = await async_quiz_client.post(
            url="/api/v1/games/create",
            headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
            json=game_request,
        )
        assert response_creation.status_code == status.HTTP_200_OK
        modes_incorrect_score[mode] += incorrect_score
        modes_correct_score[mode] += correct_score
        game_request = {
            "correct_score": modes_correct_score[mode],
            "incorrect_score": modes_incorrect_score[mode],
        }
        response_score_creation = await async_quiz_client.patch(
            url=f"/api/v1/stats/{user_sub_id}/{mode}",
            headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
            json=game_request,
        )
        assert response_score_creation.status_code == status.HTTP_200_OK

    response = await async_quiz_client.get(
        url=f"/api/v1/stats/all/{user_sub_id}",
        headers={"Authorization": f"Bearer {common_user_tokens['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    for mode in modes_list:
        if (modes_incorrect_score[mode] == 0) and (modes_correct_score[mode] == 0):
            continue
        score_dictionary = {
            "mode": mode,
            "correct_score": str(modes_correct_score[mode]),
            "incorrect_score": str(modes_incorrect_score[mode]),
        }
        assert score_dictionary in response.json()
