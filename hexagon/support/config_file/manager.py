import os
from typing import Any, Dict, Optional

from ruamel.yaml import YAML


class ConfigFileManager:
    """
    Manages reading and writing of YAML config files.

    Provides a simple interface for loading, modifying and persisting
    YAML configuration files. Intended to be reused across hexagon
    for any user-editable config file (e.g. cli_options.yml).
    """

    def __init__(self, path: str):
        self.path = path
        self._yaml = YAML()
        self._yaml.default_flow_style = False
        self._content: Optional[Any] = None

    @property
    def exists(self) -> bool:
        return os.path.isfile(self.path)

    def load(self) -> Optional[Dict[str, Any]]:
        """Load and return file contents as a plain dict, or None if file missing."""
        if not self.exists:
            return None
        with open(self.path, "r") as f:
            self._content = self._yaml.load(f)
        if self._content is None:
            return {}
        return dict(self._content)

    def get(self, key: str, default: Any = None) -> Any:
        """Return value for *key* from the loaded content."""
        data = self._content if self._content is not None else (self.load() or {})
        return data.get(key, default)

    def set_value(self, key: str, value: Any) -> None:
        """Set *key* to *value* in memory (call :meth:`save` to persist)."""
        if self._content is None:
            self._content = self._yaml.load(open(self.path)) if self.exists else {}
        self._content[key] = value

    def unset_value(self, key: str) -> bool:
        """Remove *key* from the in-memory content. Returns True if key existed."""
        if self._content is None:
            self._content = self._yaml.load(open(self.path)) if self.exists else {}
        if key in self._content:
            del self._content[key]
            return True
        return False

    def save(self) -> None:
        """Persist current in-memory content to disk, creating parent dirs if needed."""
        (
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            if os.path.dirname(self.path)
            else None
        )
        with open(self.path, "w") as f:
            self._yaml.dump(self._content or {}, f)

    def create(self, initial_content: Optional[Dict[str, Any]] = None) -> None:
        """Create the file with *initial_content* (empty dict by default)."""
        self._content = initial_content or {}
        self.save()
