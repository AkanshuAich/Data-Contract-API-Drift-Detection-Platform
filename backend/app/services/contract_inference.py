from typing import Any, Dict, List

def infer_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "number"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


def infer_structure(data: Any) -> Any:
    """
    Recursively infer JSON structure
    """
    if isinstance(data, dict):
        return {
            key: infer_structure(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        if not data:
            return []
        # infer structure from first element (practical tradeoff)
        return [infer_structure(data[0])]

    return infer_type(data)
