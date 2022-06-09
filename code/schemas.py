from pydantic import BaseModel
from typing import Optional


class CodeSchema(BaseModel):
    code: str
    user: int
    language: int
    id: Optional[int] = None
