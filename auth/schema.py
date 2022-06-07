
from pydantic import BaseModel
from typing import Optional


class PydanticUser(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None
    is_admin: Optional[bool] = False
