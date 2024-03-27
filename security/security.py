import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import Field, Model, AIOEngine
from dotenv import load_dotenv
from argon2 import PasswordHasher
import re
from bson import ObjectId

load_dotenv()
SECURITY_URI = os.getenv('MONGO_SECURITY_URLS')
SECURITY_CLIENT = AsyncIOMotorClient(SECURITY_URI)
security_engine = AIOEngine(client=SECURITY_CLIENT, database=os.getenv('MONGO_SECURITY_DB'))
argon2_hash_pattern = re.compile(r'\$argon2id\$v=(\d+)\$m=(\d+),t=(\d+),p=(\d+)\$([A-Za-z0-9+/]+)\$([A-Za-z0-9+/]+)')
argon2_hash_len = int(os.getenv('ARGON2_HASHLEN'))
argon2_salt_len = int(os.getenv('ARGON2_SALTLEN'))
argon2_parameters = os.getenv('ARGON2_PARAMETERS')
security_algorithm = PasswordHasher(hash_len=argon2_hash_len, salt_len=argon2_salt_len)


class Salt(Model):
  salt: str

async def hash_users_password(password: str, users_id: ObjectId):

  hash = security_algorithm.hash(password=password)
  match = argon2_hash_pattern.match(hash)
  if match:
    version, memory_cost, time_cost, parallelism, salt, hashed_password = match.groups()
    new_salt = Salt(id=users_id, salt=f"{salt}")
    print(users_id)
    users_salt = await security_engine.save(new_salt)
    return hashed_password
  else:
      return None
  
async def verify_users_password(password: str, users_id: ObjectId, hashed_password: str) -> bool:
  # print(users_id)
  print(argon2_parameters)
  users_salt_record = await security_engine.find_one(Salt, Salt.id == users_id)
  
  if users_salt_record != None:
    complete_argon2_hashed_password = f"{argon2_parameters}${users_salt_record.salt}${hashed_password}"
    # print(complete_argon2_hashed_password)
    if (security_algorithm.verify(complete_argon2_hashed_password, password)):
      return True
    else:
      return False