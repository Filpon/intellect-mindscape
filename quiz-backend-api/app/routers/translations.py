from fastapi import APIRouter

from app.utils.keydb import keydb_instance

router = APIRouter()


@router.get("/{language}")
async def get_translations(language: str):
    """
    Retrieve translations for the specified language.

    The endpoint fetches all translation entries stored in KeyDB for the
    given language. It returns dictionary where the keys are the translation
    identifiers and the values are the corresponding translated strings

    :param str language: The language code for retrieved translations

    :return Dict[str, str]: Dictionary containing translation identifiers as keys and
             their corresponding translated strings as values
    """
    keys = keydb_instance.keys(f"translations:{language}:*")
    translations = {
        key.decode("utf-8").split(":")[-1]: keydb_instance.get(key).decode("utf-8")
        for key in keys
    }
    return translations
