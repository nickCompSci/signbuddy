from pydantic import BaseModel

class LetterRequest(BaseModel):
    image: str
    letter: str
    apiKey: str