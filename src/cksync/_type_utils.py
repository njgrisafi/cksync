from typing import Any, TypeVar

D = TypeVar("D")

JSON_PARSABLE = TypeVar("JSON_PARSABLE", bound=dict[str, Any] | list[Any] | str | int | float | bool | None)


def verify_type(data: JSON_PARSABLE, expected_type: type[D]) -> D:
    if isinstance(data, expected_type):
        return data
    raise ValueError(f"Expected {expected_type.__name__}, got {type(data).__name__}")
