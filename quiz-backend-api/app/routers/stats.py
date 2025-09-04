from fastapi import APIRouter, Depends

from app.database.schemas import GameScoreResult
from app.services.game import oauth2_scheme
from app.utils.keydb import keydb_instance

router = APIRouter()


@router.get("/all/{user_sub_id}")
def fetch_all_user_data(user_sub_id, _: str = Depends(oauth2_scheme)):
    """
    Fetch all user data based on the provided user subscription ID.

    The endpoint retrieves all user-related data stored in KeyDB for the specified
    user subscription ID. It collects all relevant keys and decodes the stored
    hash maps into a list of dictionaries

    :param str user_sub_id: The subscription ID of the user fetched data
    :param str _: The OAuth2 token dependency for authentication

    :return List[Dict[str, str]]: List of user data entries, where each entry is a dictionary
             containing the user details
    """
    # Retrieve the data from Redis
    user_data = []
    keys = keydb_instance.keys(f"*{user_sub_id}--*")
    for key in keys:
        # Retrieve the hash map for each key
        retrieved_entry = keydb_instance.hgetall(key)
        if retrieved_entry:
            # Decode bytes to strings
            user_data.append(
                {
                    k.decode("utf-8"): v.decode("utf-8")
                    for k, v in retrieved_entry.items()
                }
            )

    if user_data:
        return user_data


@router.get("/{user_sub_id}/{mode}")
def fetch_current_mode_user_data(
    mode: str, user_sub_id, _: str = Depends(oauth2_scheme)
) -> dict | None:
    """
    Fetch user data for the current mode based on the user subscription ID.

    The endpoint retrieves the user data associated with a specific mode
    for the given user subscription ID from KeyDB. It returns the data as
    a dictionary, including the mode information

    :param str mode: The mode for which user data is to be retrieved
    :param str user_sub_id: The subscription ID of the user
    :param str _: The OAuth2 token dependency for authentication

    :return dict | None: Dictionary containing the user data for the specified mode,
             or None if no data is found
    """
    # Retrieve the data from Redis
    current_mode_user_data = None
    retrieved_entry = keydb_instance.hgetall(f"{user_sub_id}--{mode}")
    if retrieved_entry:
        current_mode_user_data = {
            k.decode("utf-8"): v.decode("utf-8") for k, v in retrieved_entry.items()
        }
        current_mode_user_data["mode"] = mode

    return current_mode_user_data


@router.patch("/{user_sub_id}/{mode}")
def update_current_mode_user_data(
    mode: str,
    game_score_result: GameScoreResult,
    user_sub_id: str,
    _: str = Depends(oauth2_scheme),
):
    """
    Update user data for the current mode based on the user subscription ID.

    The endpoint updates the user data in KeyDB for a specific mode
    using the provided game score results. It sets multiple fields in the
    hash associated with the user subscription ID and mode

    :param str mode: The mode for which user data is to be updated
    :param GameScoreResult game_score_result: The result object containing game score details
    :param str user_sub_id: The user subscription ID
    :param str _: The OAuth2 token dependency for authentication
    """
    # Retrieve the data from Redis
    game_score_result_dictionary = game_score_result.dict()
    key = f"{user_sub_id}--{mode}"
    # Using hsetall to set multiple fields in the hash
    keydb_instance.hset(
        key,
        mapping={
            "mode": mode,
            "correct_score": game_score_result_dictionary["correct_score"],
            "incorrect_score": game_score_result_dictionary["incorrect_score"],
        },
    )
