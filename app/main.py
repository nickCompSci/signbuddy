from datetime import datetime

from bson import ObjectId 

from typing import Annotated
from dotenv import load_dotenv

from fastapi import  FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response


from .services import AsyncHttpClient, MONGODB_ENGINE
from .helpers import CreateAlphabetCourseForUser, fetchSecrets
from .models import  AlphabetCourse, LetterRequest, LetterResponse, PatchLetter
from .security import authenticateUser, obtainModelBearerToken, decodeJwt


app = FastAPI()
load_dotenv()

LETTER_INFERENCE_API_URL = fetchSecrets("LETTER_INFERENCE_API_URL")

AUTH0_MANAGEMENT_API_ENDPOINT = fetchSecrets("AUTH0_MANAGEMENT_ENDPOINT")

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    fetchSecrets("ALLOWED_ORIGINS")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


async def decode_jwt(token: Annotated[str, Depends(OAUTH2_SCHEME)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': "Bearer"},
    )
    try:
        payload = decodeJwt(token=token)

    except Exception:
        raise credentials_exception

    isUsersId = payload.get("sub")

    if isUsersId is None:
        raise credentials_exception
    user = await authenticateUser(isUsersId)

    if user is None:
        raise credentials_exception

    return user

@app.get("/alphabetcourse", status_code=status.HTTP_200_OK)
async def alphabet_course(current_user: Annotated[object, Depends(decode_jwt)], response: Response):
    try:
        currentUsersId = current_user["user_id"]
        actualId = currentUsersId.split('|')[1]
        usersAlphabet = await MONGODB_ENGINE.find_one(AlphabetCourse, AlphabetCourse.id==ObjectId(actualId))
        if usersAlphabet:
            return {"alphabet": usersAlphabet}
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}

@app.get("/checkcourse", status_code=status.HTTP_200_OK)
async def check_course(current_user: Annotated[object, Depends(decode_jwt)],response: Response):
    try:
        currentUsersId = current_user["user_id"]
        actualId = currentUsersId.split('|')[1]
        
        usersAlphabet = await MONGODB_ENGINE.find_one(AlphabetCourse, AlphabetCourse.id==ObjectId(actualId))
        if usersAlphabet:
            return
        else:
            users_alphabet_course = CreateAlphabetCourseForUser(ObjectId(actualId))
            await MONGODB_ENGINE.save(users_alphabet_course)
            return
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}
    
@app.post("/updateletter", response_model=LetterResponse)
async def checkletter(current_user: Annotated[object, Depends(decode_jwt)], incomingLetter: LetterRequest, request: Request):
    currentUsersId = current_user["user_id"]
    actualId = ObjectId(currentUsersId.split('|')[1])

    signBuddyModelBearerToken = await obtainModelBearerToken()
  
    userLetter = incomingLetter.letter
    modelApiResponseResult = ""
    jsonDataToSend = {"image": incomingLetter.image, "letter": userLetter}
    
    async with AsyncHttpClient() as client:
        modelApiResponseResult = await client.post_image(LETTER_INFERENCE_API_URL, data=jsonDataToSend, bearerToken=signBuddyModelBearerToken)

     
    # obtain users alphabet course
    users_alphabet_course = await MONGODB_ENGINE.find_one(AlphabetCourse, AlphabetCourse.id==actualId)
    isUserLetterCorrect = modelApiResponseResult["letterResult"]
    
    newSuccessfulAttempts = users_alphabet_course.letters[userLetter].successfulAttempts
    newTotalSuccessfulAttempts = users_alphabet_course.letters[userLetter].totalSuccessful
    newFailedAttempts = users_alphabet_course.letters[userLetter].failedAttempts
    isUserCompleted = users_alphabet_course.letters[userLetter].completed
    date = users_alphabet_course.letters[userLetter].date_completed;
    if isUserLetterCorrect == 1:
        newTotalSuccessfulAttempts += 1
        if newSuccessfulAttempts < 3:
            newSuccessfulAttempts += 1

    else:
        if not isUserCompleted == 1:
            newFailedAttempts +=1
            if newFailedAttempts >= users_alphabet_course.letters[userLetter].failQuota:
                newSuccessfulAttempts = 0
                newFailedAttempts = 0
    newTotalAttempts = users_alphabet_course.letters[userLetter].totalAttempts + 1
    
    if newSuccessfulAttempts >= 3 and not isUserCompleted == 1:
        isUserCompleted = 1
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        currentProgess = users_alphabet_course.progress
        newCurrentProgress = currentProgess + (1/26 * 100)
        if newCurrentProgress >= 98.0:
            newCurrentProgress = 100
        patchDict = {"progress": newCurrentProgress}
        users_alphabet_course.model_update(patchDict)
        await MONGODB_ENGINE.save(users_alphabet_course)

    patchObject = PatchLetter(completed=isUserCompleted, successfulAttempts=newSuccessfulAttempts, failedAttempts=newFailedAttempts, totalSuccessful=newTotalSuccessfulAttempts, totalAttempts=newTotalAttempts, date_completed=date)

    users_alphabet_course.letters[userLetter] = patchObject

    users_alphabet_course.model_update(users_alphabet_course.letters[userLetter])
    await MONGODB_ENGINE.save(users_alphabet_course)
    letterResponse = LetterResponse(letterResult=patchObject, resultImage=modelApiResponseResult["image"], letterAttempt=modelApiResponseResult["letterResult"])
    return letterResponse
    