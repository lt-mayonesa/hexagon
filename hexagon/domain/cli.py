from typing import Optional

from pydantic import BaseModel


class Cli(BaseModel):
    name: str
    command: str
    custom_tools_dir: Optional[str] = None
    plugins_dir: Optional[str] = None
