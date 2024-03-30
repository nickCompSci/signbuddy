from jose import jwt
from dotenv import load_dotenv
from ..helpers import fetchSecrets

load_dotenv()

JWT_APPLICATION_AUDIENCE=fetchSecrets("JWT_APPLICATION_AUDIENCE")
JWT_APPLICATION_ISSUER=fetchSecrets("JWT_APPLICATION_ISSUER")
JWT_APPLICATION_KEY=fetchSecrets("JWT_APPLICATION_KEY")
JWT_ALGORITHMS=fetchSecrets("JWT_ALGORITHMS")

def decodeJwt(token:str):
  try:
    payload = jwt.decode(token=token, audience=JWT_APPLICATION_AUDIENCE, issuer=JWT_APPLICATION_ISSUER, key=JWT_APPLICATION_KEY, algorithms=[JWT_ALGORITHMS])
    return payload
  except:
    raise Exception