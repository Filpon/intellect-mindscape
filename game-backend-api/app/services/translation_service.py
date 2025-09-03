import json

from app.configs.logging_handler import configure_logging_handler
from app.utils.keydb import keydb_instance

logger = configure_logging_handler()


def load_translations_key_db(file_path: str) -> None:
    """
    Loading translations from JSON file and store them in cache database

    :param str file_path: The path to containing translations JSON file
    """
    try:
        logger.info("file_path=%s", file_path)
        translations = {}
        # Translations to load into KeyDB
        with file_path.open(mode="r", encoding="utf-8") as file:
            translations = json.load(file)
        logger.info("file_translations=%s", translations)
        for key, value in translations.items():
            for lang, text in value.items():
                keydb_instance.set(f"translations:{lang}:{key}", text)
    except FileNotFoundError:
        print("Error: The translations.json file was not found")
    except json.JSONDecodeError:
        print("Error: The translations.json file is not a valid JSON")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
