# exceptions.py
from fastapi import HTTPException

class InvalidCredentialsException(HTTPException):
    """
    Exception raised for invalid credentials during authentication.

    This exception is used to indicate that the provided username or password
    is incorrect when attempting to log in.
    """
    def __init__(self):
        """
        Initializes the InvalidCredentialsException with a 401 status code
        and a detail message indicating invalid credentials.
        """
        super().__init__(status_code=401, detail="Invalid credentials")
