from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from ..helpers import fetchSecrets

MONGODB_URI = f"{fetchSecrets('MONGO_URI_FULL')}retryWrites=true&w=majority&appName={fetchSecrets('MONGO_URI_APPNAME')}"
MONGODB_CLIENT = AsyncIOMotorClient(MONGODB_URI)

MONGODB_ENGINE = AIOEngine(client=MONGODB_CLIENT, database=fetchSecrets('MONGO_DBNAME'))
