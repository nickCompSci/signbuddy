from ..services import AsyncHttpClient
from dotenv import load_dotenv
from .FetchSecrets import fetchSecrets

load_dotenv()

AUTH0_MANAGEMENT_CLIENT_ID=fetchSecrets("AUTH0_MANAGEMENT_CLIENT_ID")
AUTH0_MANAGEMENT_CLIENT_SECRET=fetchSecrets("AUTH0_MANAGEMENT_CLIENT_SECRET")
AUTH0_MANAGEMENT_AUDIENCE=fetchSecrets("AUTH0_MANAGEMENT_AUDIENCE")
AUTH0_MANAGEMENT_GRANT_TYPE=fetchSecrets("AUTH0_MANAGEMENT_GRANT_TYPE")
AUTH0_MANAGEMENT_ENDPOINT=fetchSecrets("AUTH0_MANAGEMENT_ENDPOINT")
AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT=fetchSecrets("AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT")

async def authenticateUser(usersId):
  credentialsData= {"grant_type": AUTH0_MANAGEMENT_GRANT_TYPE, "client_id": AUTH0_MANAGEMENT_CLIENT_ID, "client_secret": AUTH0_MANAGEMENT_CLIENT_SECRET, "audience": AUTH0_MANAGEMENT_AUDIENCE}
  async with AsyncHttpClient() as client:
      modelApiResponseResult = await client.post_auth0_management_api_token(AUTH0_MANAGEMENT_ENDPOINT, data=credentialsData)
      auth0BearerToken = modelApiResponseResult['access_token']
  user = ""
  async with AsyncHttpClient() as client:
      user = await client.get_current_user(f"{AUTH0_MANAGEMENT_CURRENT_USER_ENDPOINT}{usersId}", data=credentialsData, bearerToken=auth0BearerToken)
  return user