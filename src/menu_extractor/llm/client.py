from cohere import AsyncClient

from menu_extractor import logger


class LLM:
    def __init__(self, cohere_client_name: str, cohere_api_key: str, cohere_model: str):
        self._client = AsyncClient(
            client_name=cohere_client_name,
            api_key=cohere_api_key,
        )
        self._cohere_model = cohere_model
        pass

    async def generate(self, system_message: str, user_message: str) -> str:
        logger.debug(
            "Sending LLM request ...",
            extra={"input_tokens": len(user_message) + len(system_message)},
        )
        response = await self._client.chat(
            message=user_message,
            model=self._cohere_model,
            preamble=system_message,
        )
        return response.text
