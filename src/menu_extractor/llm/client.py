from cohere import AsyncClient

from menu_extractor import logger
from menu_extractor.llm.prompts import SYSTEM, USER


class LLM:
    def __init__(self, cohere_client_name: str, cohere_api_key: str, cohere_model: str):
        self._client = AsyncClient(
            client_name=cohere_client_name,
            api_key=cohere_api_key,
        )
        self._cohere_model = cohere_model
        pass

    async def extract_structured_data_string_from_menu_page(
        self, menu_page: str
    ) -> str:
        logger.debug(
            "Sending LLM request ...",
            extra={"pdf_page_characters": len(menu_page)},
        )
        response = await self._client.chat(
            message=USER.format(menu_page=menu_page),
            model=self._cohere_model,
            preamble=SYSTEM,
        )
        return response.text
