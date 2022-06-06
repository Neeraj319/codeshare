
from pydantic import BaseModel
from typing import Optional


class PydanticUser(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    is_admin: Optional[bool] = False
