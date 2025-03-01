from menu_extractor import logger
from menu_extractor.exceptions import (
    InvalidGPTMenuItemResponseError,
)
from menu_extractor.models import MenuItemList


def parse_dict_str_from_llm_response(llm_response: str) -> MenuItemList:
    output = llm_response.replace("```json", "```").split("```")
    if len(output) > 1:
        output = output[1]
    else:
        logger.warning(
            "No backticks (```) detected in llm response. Attempting to parse...",
            colorize=True,
        )
        output = output[0]
    try:
        menu_items = MenuItemList.model_validate_json(output)
    except Exception as e:
        # todo: reraise and err handling
        raise InvalidGPTMenuItemResponseError(e)

    return menu_items
