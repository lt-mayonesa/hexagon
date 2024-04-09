from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class EntrypointConfig(BaseModel):
    shell: Optional[str] = None
    pre_command: Optional[str] = None
    environ: Dict[str, Any] = {}


class Cli(BaseModel):
    name: str
    command: str
    entrypoint: EntrypointConfig = EntrypointConfig()
    custom_tools_dir: Optional[str] = None
    plugins: List[str] = []
    options: Optional[dict] = None
