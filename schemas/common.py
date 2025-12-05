from pydantic import BaseModel
from typing import Optional, Any

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    # access_token: Optional[str] = None
    # token_type: Optional[str] = None