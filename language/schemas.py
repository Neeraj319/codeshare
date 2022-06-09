from pydantic import BaseModel
from typing import Optional


class LanguageSchema(BaseModel):
    name: str
    id: Optional[int] = None
