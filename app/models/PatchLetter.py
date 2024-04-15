from pydantic import BaseModel
from typing import Optional

class PatchLetter(BaseModel):
    completed: int
    successfulAttempts: int
    failedAttempts: int
    failQuota: int = 2
    totalAttempts: int
    totalSuccessful: int
    date_completed: Optional[str] = None