"""Configuration parsing and validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from errors import ConfigError

Position: TypeAlias = tuple[int, int]

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


@dataclass(frozen=True)
class Config:
    """Validated values loaded from a configuration file."""

    width: int
    height: int
    entry: Position
    exit: Position
    output_file: Path
    perfect: bool
    seed: int | None = None

    @classmethod
    def from_file(cls, filename: str) -> "Config":
        """Read and validate a configuration file."""

        try:
            contents = Path(filename).read_text(encoding="utf-8")
        except OSError as exc:
            raise ConfigError(
                f"cannot read configuration file '{filename}': {exc}"
            ) from exc

        values: dict[str, str] = {}
        for line_number, raw_line in enumerate(contents.splitlines(), 1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(
                    f"line {line_number}: expected KEY=VALUE"
                )

            key, value = (part.strip() for part in line.split("=", 1))
            key = key.upper()
            if not key or not value:
                raise ConfigError(
                    f"line {line_number}: key and value must not be empty"
                )
            if key in values:
                raise ConfigError(f"line {line_number}: duplicate key '{key}'")
            values[key] = value

        missing = sorted(REQUIRED_KEYS - values.keys())
        if missing:
            raise ConfigError(
                "missing mandatory configuration keys: " + ", ".join(missing)
            )

        width = _parse_positive_int(values["WIDTH"], "WIDTH")
        height = _parse_positive_int(values["HEIGHT"], "HEIGHT")
        entry = _parse_position(values["ENTRY"], "ENTRY")
        exit_position = _parse_position(values["EXIT"], "EXIT")
        _validate_position(entry, width, height, "ENTRY")
        _validate_position(exit_position, width, height, "EXIT")
        if entry == exit_position:
            raise ConfigError("ENTRY and EXIT must be different")

        output_file = Path(values["OUTPUT_FILE"])
        if not str(output_file):
            raise ConfigError("OUTPUT_FILE must not be empty")

        perfect = _parse_bool(values["PERFECT"], "PERFECT")
        seed = None
        if "SEED" in values:
            seed = _parse_int(values["SEED"], "SEED")

        return cls(
            width=width,
            height=height,
            entry=entry,
            exit=exit_position,
            output_file=output_file,
            perfect=perfect,
            seed=seed,
        )


def _parse_positive_int(value: str, key: str) -> int:
    parsed = _parse_int(value, key)
    if parsed <= 0:
        raise ConfigError(f"{key} must be positive")
    return parsed


def _parse_int(value: str, key: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer: '{value}'") from exc


def _parse_position(value: str, key: str) -> Position:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 2:
        raise ConfigError(f"{key} must use x,y format")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise ConfigError(f"{key} must use integer coordinates") from exc


def _validate_position(
    position: Position,
    width: int,
    height: int,
    key: str,
) -> None:
    x, y = position
    if not (0 <= x < width and 0 <= y < height):
        raise ConfigError(f"{key} must be inside the maze")


def _parse_bool(value: str, key: str) -> bool:
    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ConfigError(f"{key} must be True or False")
