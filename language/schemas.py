from pydantic import BaseModel
from typing import Optional


class LanguageSchema(BaseModel):
    name: str
    id: Optional[int] = None


class LanguageUpdateSchema(BaseModel):
    name: Optional[str] = None
    language_id: Optional[int] = None
