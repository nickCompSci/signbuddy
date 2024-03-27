from services import AsyncHttpClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

AUTH0_SIGNBUDDY_MODEL_CLIENT_ID=getenv("AUTH0_SIGNBUDDY_MODEL_CLIENT_ID")
AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET=getenv("AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET")
AUTH0_SIGNBUDDY_MODEL_AUDIENCE=getenv("AUTH0_SIGNBUDDY_MODEL_AUDIENCE")
AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE=getenv("AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE")
AUTH0_MANAGEMENT_ENDPOINT=getenv("AUTH0_MANAGEMENT_ENDPOINT")

async def obtainModelBearerToken():
  async with AsyncHttpClient() as client:
    credentialsData = {"client_id": AUTH0_SIGNBUDDY_MODEL_CLIENT_ID, "client_secret": AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET, "audience": AUTH0_SIGNBUDDY_MODEL_AUDIENCE, "grant_type": AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE}
    try:
      modelApiResponseResult = await client.post_auth0_signbuddymodel_api_token(AUTH0_MANAGEMENT_ENDPOINT, data=credentialsData)
      signBuddyModelBearerToken = modelApiResponseResult['access_token']
      return signBuddyModelBearerToken
    except Exception:
      raise Exception
    
