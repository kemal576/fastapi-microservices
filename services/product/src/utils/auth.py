from fastapi import Depends, Header, HTTPException, status

from src.config import Settings


class CustomHeaderParams:
    def __init__(
        self,
        X_API_KEY: str = Header(..., description="Api Key"),
    ):
        self.X_API_KEY = X_API_KEY


def api_key_auth(header_params: CustomHeaderParams = Depends()):
    api_key: str = header_params.X_API_KEY
    if api_key != Settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")
