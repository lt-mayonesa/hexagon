from typing import Optional, List

from pydantic import BaseModel


class Cli(BaseModel):
    name: str
    command: str
    custom_tools_dir: Optional[str] = None
    plugins: List[str] = []
    options: Optional[dict] = None
