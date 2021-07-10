from typing import Optional

from pydantic import BaseModel


class Env(BaseModel):
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
