from fastapi import APIRouter, Depends

from app.services.game import oauth2_scheme
from app.utils.keydb import keydb_instance

router = APIRouter()


@router.get("/{user_sub_id}")
def get_user_data(user_sub_id, _: str = Depends(oauth2_scheme)):
    # Retrieve the data from Redis
    user_data = []
    keys = keydb_instance.keys(f"*{user_sub_id}-recommendations*")
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
