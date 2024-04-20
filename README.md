# Python, FastAPI, Docker

This project houses the main backend API for the SignBuddy application

To run this project do the following:

1. Create a python virtual environment; `python -m venv venv`
2. Activate venv; `.\venv\Scripts\activate` on windows
3. Run `pip install -r requirements.txt`
4. Create a .env file with necessary environment variables.
5. Run `uvicorn app.main:app --port 3000 --reload`

## References

- All code was custom developed or was developed by following tutorials from official sources such as FastAPI, Python and Docker