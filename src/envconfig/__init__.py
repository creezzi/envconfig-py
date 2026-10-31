"""Typed environment configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

__all__ = ["Var", "load", "ConfigError"]

_REQUIRED = object()
_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off", ""}


class ConfigError(Exception):
    def __init__(self, problems: List[str]):
        super().__init__("invalid configuration:\n  " + "\n  ".join(problems))
        self.problems = problems


@dataclass(frozen=True)
class Var:
    type: type = str
    default: Any = _REQUIRED
    separator: str = ","

    def convert(self, raw: str) -> Any:
        if self.type is bool:
            lowered = raw.strip().lower()
            if lowered in _TRUE:
                return True
            if lowered in _FALSE:
                return False
            raise ValueError(f"expected a boolean, got {raw!r}")
        if self.type is list:
            return [p.strip() for p in raw.split(self.separator) if p.strip()]
        return self.type(raw)


def load(schema: Mapping[str, Var], environ: Optional[Mapping[str, str]] = None) -> Dict[str, Any]:
    """Read every variable in `schema`; raise one ConfigError listing all failures."""
    env = os.environ if environ is None else environ
    values: Dict[str, Any] = {}
    problems: List[str] = []
    for name, var in schema.items():
        if name not in env:
            if var.default is _REQUIRED:
                problems.append(f"{name} is required")
            else:
                values[name] = var.default
            continue
        try:
            values[name] = var.convert(env[name])
        except (ValueError, TypeError) as exc:
            problems.append(f"{name}: {exc}")
    if problems:
        raise ConfigError(problems)
    return values
