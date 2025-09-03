from fastapi import APIRouter, Depends

from app.database.schemas import GameScoreResult
from app.services.game import oauth2_scheme
from app.utils.keydb import keydb_instance

router = APIRouter()


@router.get("/all/{user_sub_id}")
def fetch_all_user_data(user_sub_id, _: str = Depends(oauth2_scheme)):
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
