from dotenv import load_dotenv
from bson import ObjectId 
from ..helpers import fetchSecrets
from ..models import managementToken
from ..services import MONGODB_ENGINE, AsyncHttpClient


load_dotenv()

AUTH0_MANAGEMENT_CLIENT_ID=fetchSecrets("AUTH0_MANAGEMENT_CLIENT_ID")
AUTH0_MANAGEMENT_CLIENT_SECRET=fetchSecrets("AUTH0_MANAGEMENT_CLIENT_SECRET")
AUTH0_MANAGEMENT_AUDIENCE=fetchSecrets("AUTH0_MANAGEMENT_AUDIENCE")
AUTH0_MANAGEMENT_GRANT_TYPE=fetchSecrets("AUTH0_MANAGEMENT_GRANT_TYPE")
AUTH0_MANAGEMENT_ENDPOINT=fetchSecrets("AUTH0_MANAGEMENT_ENDPOINT")
AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT=fetchSecrets("AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT")
CREDENTIALS_DATA= {"grant_type": AUTH0_MANAGEMENT_GRANT_TYPE, "client_id": AUTH0_MANAGEMENT_CLIENT_ID, "client_secret": AUTH0_MANAGEMENT_CLIENT_SECRET, "audience": AUTH0_MANAGEMENT_AUDIENCE}
MONGO_MAPI_TOKEN_ID= fetchSecrets("MONGO_MAPI_TOKEN_ID")

async def authenticateUser(usersId):
  user = None
  result = await MONGODB_ENGINE.find_one(managementToken, managementToken.id == ObjectId(MONGO_MAPI_TOKEN_ID))
  if result:
      auth0BearerToken = result.access_token
      userTemp = await getUser(usersId, auth0BearerToken)
      if userTemp == -1:
        auth0BearerToken = await obtainMangementApiToken()
        user = await getUser(usersId, auth0BearerToken)
      else:
          user = userTemp
  return user

async def obtainMangementApiToken():
    async with AsyncHttpClient() as client:
        modelApiResponseResult = await client.post_auth0_management_api_token(AUTH0_MANAGEMENT_ENDPOINT, data=CREDENTIALS_DATA)
        auth0BearerToken = modelApiResponseResult['access_token']
        newToken = managementToken(id=ObjectId(MONGO_MAPI_TOKEN_ID), access_token=auth0BearerToken)
        await MONGODB_ENGINE.save(newToken)
        return auth0BearerToken
    
async def getUser(usersId, auth0BearerToken):
  try:
    async with AsyncHttpClient() as client:
        user = await client.get_current_user(f"{AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT}{usersId}", data=CREDENTIALS_DATA, bearerToken=auth0BearerToken)
        if user == None:
            return -1     
        return user
  except Exception as ex:
      raise ex
