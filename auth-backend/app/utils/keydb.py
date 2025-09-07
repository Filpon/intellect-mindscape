import os

from redis import StrictRedis

KEYDB_PASSWORD = os.getenv("KEYDB_PASSWORD")

# Connect to KeyDB
keydb_instance = StrictRedis(host="keydb", port=6379, password=KEYDB_PASSWORD)
