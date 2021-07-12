from typing import Optional

from pydantic import BaseModel


class Env(BaseModel):
    name: str
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
