import re
from typing import Any, Sequence, TypeVar

import json5
from pydantic import BaseModel, TypeAdapter

from .exceptions import InvalidBacktickFormatError

T = TypeVar("T", bound=BaseModel | Sequence[BaseModel])


def parse_text_to_model(text: str, model_class: type[T]) -> T:
    """
    Parses the provided JSON5 string (which may be wrapped in backticks) into a Pydantic model.

    Args:
    - text (str): The JSON5 string, potentially wrapped in backticks.
    - model_class (type[T]): The Pydantic model class to convert the parsed data into.

    Returns:
    - An instance of the provided Pydantic model class, validated with the parsed data.
    """
    json5_content = _extract_json_from_backticks(text)

    model_adapter = TypeAdapter(model_class)

    try:
        parsed_data: Any = json5.loads(json5_content)
    except Exception:
        raise ValueError("The text could not be loaded.")

    return model_adapter.validate_python(parsed_data)


def _extract_json_from_backticks(text: str) -> str:
    """
    Extracts JSON5 content from text that is wrapped in exactly one pair of backticks.
    """
    text = text.replace("```json", "```")

    backtick_pattern = r"```(.*?)```"

    matches = re.findall(backtick_pattern, text, re.DOTALL)

    if len(matches) != 1:
        raise InvalidBacktickFormatError(
            "Text must contain exactly one pair of backticks."
        )

    return matches[0]
