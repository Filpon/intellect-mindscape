from fastapi import APIRouter

from app.utils.keydb import keydb_instance

router = APIRouter()


@router.get("/{language}")
async def get_translations(language: str):
    keys = keydb_instance.keys(f"translations:{language}:*")
    translations = {
        key.decode("utf-8").split(":")[-1]: keydb_instance.get(key).decode("utf-8")
        for key in keys
    }
    return translations
