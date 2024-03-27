from odmantic import EmbeddedModel
from typing import Optional

class Letter(EmbeddedModel):
    completed: int = -1
    successfulAttempts: int
    failedAttempts: int
    failQuota: int = 2
    totalAttempts: int
    totalSuccessful: int
    date_completed: Optional[str] = None