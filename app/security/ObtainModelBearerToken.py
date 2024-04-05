from dotenv import load_dotenv
from bson import ObjectId 
from ..helpers import fetchSecrets
from ..services import MONGODB_ENGINE, AsyncHttpClient
from ..models import ModelToken

load_dotenv()

AUTH0_SIGNBUDDY_MODEL_CLIENT_ID=fetchSecrets("AUTH0_SIGNBUDDY_MODEL_CLIENT_ID")
AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET=fetchSecrets("AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET")
AUTH0_SIGNBUDDY_MODEL_AUDIENCE=fetchSecrets("AUTH0_SIGNBUDDY_MODEL_AUDIENCE")
AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE=fetchSecrets("AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE")
AUTH0_MANAGEMENT_ENDPOINT=fetchSecrets("AUTH0_MANAGEMENT_ENDPOINT")
MONGO_MODEL_API_TOKEN_ID=fetchSecrets("MONGO_MODEL_API_TOKEN_ID")
LETTER_INFERENCE_API_URL=fetchSecrets("LETTER_INFERENCE_API_URL")

async def sendLetterForResult(jsonDataToSend):

  result = await MONGODB_ENGINE.find_one(ModelToken, ModelToken.id== ObjectId(MONGO_MODEL_API_TOKEN_ID))
  
  if result:
    signBuddyModelBearerToken = result.access_token
    letterRequestResult = await sendLetter(jsonDataToSend=jsonDataToSend, signBuddyModelBearerToken=signBuddyModelBearerToken)
    if letterRequestResult is None:
      signBuddyModelBearerToken = await obtainToken()
      letterRequestResult = await sendLetter(jsonDataToSend=jsonDataToSend, signBuddyModelBearerToken=signBuddyModelBearerToken)
    return letterRequestResult
  else:
    signBuddyModelBearerToken = await obtainToken()
    newToken = ModelToken(id=ObjectId(MONGO_MODEL_API_TOKEN_ID), access_token=signBuddyModelBearerToken)
    await MONGODB_ENGINE.save(newToken)
    
async def obtainToken():
  async with AsyncHttpClient() as client:
    credentialsData = {"client_id": AUTH0_SIGNBUDDY_MODEL_CLIENT_ID, "client_secret": AUTH0_SIGNBUDDY_MODEL_CLIENT_SECRET, "audience": AUTH0_SIGNBUDDY_MODEL_AUDIENCE, "grant_type": AUTH0_SIGNBUDDY_MODEL_GRANT_TYPE}
    try:
      modelApiResponseResult = await client.post_auth0_signbuddymodel_api_token(AUTH0_MANAGEMENT_ENDPOINT, data=credentialsData)
      signBuddyModelBearerToken = modelApiResponseResult['access_token']
      newToken = ModelToken(id=ObjectId(MONGO_MODEL_API_TOKEN_ID), access_token=signBuddyModelBearerToken)
      await MONGODB_ENGINE.save(newToken)
      return signBuddyModelBearerToken
    except Exception:
      raise Exception
    
async def sendLetter(jsonDataToSend, signBuddyModelBearerToken):
    async with AsyncHttpClient() as client:
        modelApiResponseResult = await client.post_image(LETTER_INFERENCE_API_URL, data=jsonDataToSend, bearerToken=signBuddyModelBearerToken)
        return modelApiResponseResult