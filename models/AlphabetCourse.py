from typing import Dict
from odmantic import Model

from .Letter import Letter

class AlphabetCourse(Model):
    name: str
    progress: float
    letters: Dict[str, Letter]