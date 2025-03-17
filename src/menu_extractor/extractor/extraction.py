"""
Given some text, extract menu items
"""

from ..llm import LLM
from ..models import MenuItem
from ..parsing import parse_text_to_model
from .prompts import SYSTEM, USER


class MenuItemExtractor:
    def __init__(self, llm_client: LLM):
        self._system_message = SYSTEM.format(
            menu_item_schema=MenuItem.formatted_schema()
        )
        self._llm = llm_client
        pass

    async def extract(self, text: str) -> list[MenuItem]:
        user_message = USER.format(menu_text=text)

        response = await self._llm.generate(
            system_message=self._system_message, user_message=user_message
        )
        with open("o.txt", "w") as file:
            file.write(response)

        result = parse_text_to_model(response, list[MenuItem])

        return result
