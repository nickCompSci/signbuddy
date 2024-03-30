from pydantic import BaseModel

from .PatchLetter import PatchLetter

class LetterResponse(BaseModel):
    letterResult: PatchLetter
    resultImage: str = None
    letterAttempt: int = -1