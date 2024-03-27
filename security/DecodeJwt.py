from jose import jwt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

JWT_APPLICATION_AUDIENCE=getenv("JWT_APPLICATION_AUDIENCE")
JWT_APPLICATION_ISSUER=getenv("JWT_APPLICATION_ISSUER")
JWT_APPLICATION_KEY=getenv("JWT_APPLICATION_KEY")
JWT_ALGORITHMS=getenv("JWT_ALGORITHMS")

def decodeJwt(token:str):
  try:
    payload = jwt.decode(token=token, audience=JWT_APPLICATION_AUDIENCE, issuer=JWT_APPLICATION_ISSUER, key=JWT_APPLICATION_KEY, algorithms=[JWT_ALGORITHMS])
    return payload
  except:
    raise Exception