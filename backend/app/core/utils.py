from base64 import b64decode, b64encode
from typing import Dict, Optional, Tuple

from app.core.config import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param


# same as fastapi.security.OAuth2PasswordBearer
# except uses `request.cookies.get("access_token")` instead of `request.headers.get("Authorization")``
# to get the token from http-only cookie
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name,
                         description=description, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # changed to accept access token from httpOnly Cookie
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


def generate_task_access_key(user_id: int, task_id: int) -> str:
    # Combine the user_id and task_id to form the data to be encrypted
    data_string = f"{user_id}:{task_id}"
    # need to convert to bytes for AES encryption
    data = data_string.encode('utf-8')
    key = settings.TASK_SECRET_KEY.encode('utf-8')
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC)  # using AES-256, the key is 32 bytes
    # pad is to fill empty bytes if the data is not 16 bytes
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    result = iv + ct_bytes
    # convert bytes to base64 string to ensure it can be safely transmitted or stored without risk of modification or data loss
    return b64encode(result).decode('utf-8')


def decipher_task_access_key(access_key: str) -> Tuple[int, int]:
    key = settings.TASK_SECRET_KEY.encode('utf-8')
    # Convert base64 string to bytes
    raw = b64decode(access_key)
    # Extract the IV and ciphertext from the raw bytes
    iv = raw[:AES.block_size]  # AES block size is 16
    ciphertext = raw[AES.block_size:]
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Decrypt the ciphertext and remove tailing empty bytes
    data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    data_string = data.decode('utf-8')
    user_id, task_id = map(int, data_string.split(':'))

    return user_id, task_id
