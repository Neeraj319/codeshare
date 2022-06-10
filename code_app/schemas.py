from pydantic import BaseModel
from typing import Optional


class CodeSchema(BaseModel):
    text: str
    language_id: int
    id: Optional[int] = None
    url: Optional[str] = None
