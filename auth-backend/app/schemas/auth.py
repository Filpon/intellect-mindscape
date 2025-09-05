from pydantic import BaseModel

class Token(BaseModel):
    """
    Representing access token and refresh token

    :param string access_token: The access token
    :param string refresh_token: The refresh token string.
    :param str token_type: The type of the token (e.g. "Bearer")
    """
    token: str


class RefreshToken(BaseModel):
    """
    Representing refresh token

    :param string refresh_token: The refresh token
    :param str token_type: The type of the token (e.g. "Bearer")
    """
    refresh_token: str
    token_type: str


class TokenInfo(BaseModel):
    """
    Model token information

    :param bool active: Indicates if the token is active
    :param int exp: The expiration time of the token as Unix timestamp
    :param int iat: The time the token was issued as a Unix timestamp
    :param string sub: The subject (user identifier) of the token
    """
    active: bool
    exp: int
    iat: int
    sub: str


class TokenResponseSchema(BaseModel):
    """
    Validation and structure of Token Response model

    :param str access_token: The access token
    :param str refresh_token: The refresh token
    :param str expires_in: The duration until the access token expires
    :param str refresh_expires_in: The duration in seconds until the refresh token expires
    :param str not_before_policy: The time before which the token is not valid
    """

    access_token: str
    refresh_token: str
    expires_in: str
    refresh_expires_in: str
    not_before_policy: str


class TokenResponseCallbackSchema(BaseModel):
    """
    Representing token validation

    :param str access_token: The access token string
    :param str id_token: The ID token string
    """

    access_token: str
    id_token: str


class User(BaseModel):
    """
    User description

    :param str username: The username
    :param bool is_active: Indicates if the user is active
    """
    username: str
    is_active: bool

    class Config:
        """
        User Config class
        """
        from_attributes = True


class UserCreate(BaseModel):
    """
    Creating new user

    :param str username: The username
    :param str password: The password for the new user
    """
    username: str
    password: str


class UserUpdate(BaseModel):
    """
    Updating user's password

    :param str new_password: The new password for the user
    """
    new_password: str


class UserInDB(User):
    """
    Representing user stored in the database

    :param str hashed_password: The hashed password of the user
    """
    hashed_password: str


class CustomOAuth2PasswordRequestForm(BaseModel):
    """
    Class representing form for OAuth2 grant type,
    containing necessary fields for user credentials

    :param str username: The username of the user
    :param str password: The password of the user
    """
    username: str
    password: str
