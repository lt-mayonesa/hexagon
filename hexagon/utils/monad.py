# For referencing a class type inside itself https://stackoverflow.com/a/33533514/2002588
from __future__ import annotations

from typing import Callable, TypeVar, Generic


T = TypeVar("T")


class IdentityMonad(Generic[T]):
    U = TypeVar("U")

    def __init__(self, value: T) -> None:
        self.value = value

    value: T

    def bind(self, f: Callable[[T], U]) -> IdentityMonad[U]:
        return IdentityMonad(f(self.value))

    def apply(self, f: Callable[[T], None]):
        f(self.value)
        return self
