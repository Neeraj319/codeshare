from pydantic import BaseModel
from typing import Optional


class CodeSchema(BaseModel):
    text: str
    language_id: int
    id: Optional[int] = None
    slug: Optional[str] = None
    user_id: Optional[int] = None


class CodeUpdateSchema(BaseModel):
    text: Optional[str] = None
    language_id: Optional[int] = None
