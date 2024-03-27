from bson import ObjectId 

from ..models import AlphabetCourse
from ..models import Letter


def CreateAlphabetCourseForUser(usersid: ObjectId):
    baseAlphabetCourse = AlphabetCourse(
    id=usersid,
    name="Alphabet",
    progress= 0.0,
    letters= {
        "A": Letter(
            successfulAttempts=0,
            failedAttempts=0,
            totalAttempts=0,
            totalSuccessful=0,
        )
    }
    )
    for letter in range(ord('B'), ord('Z') + 1):
        letter_char = chr(letter)
        baseAlphabetCourse.letters[letter_char] = Letter(
            successfulAttempts=0,
            failedAttempts=0,
            totalAttempts=0,
            totalSuccessful=0,
        )
    return baseAlphabetCourse