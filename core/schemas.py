from pydantic import BaseModel
from typing import Optional
from auth.schemas import PydanticUser


class LanguageSchema(BaseModel):
    name: str
    id: Optional[int] = None


class CodeSchema(BaseModel):
    code: str
    user: int
    language: int
    id: Optional[int] = None
