import asyncio
from pathlib import Path

from menu_extractor import logger, secrets
from menu_extractor.chunker import PdfChunker
from menu_extractor.extractor import MenuItemExtractor
from menu_extractor.llm import LLM
from menu_extractor.models import Menu, MenuItem


async def pdf_to_menu(pdf_path: Path) -> Menu:
    """The entry point to run the menu extraction process."""

    llm = LLM(
        cohere_api_key=secrets.cohere_settings__api_key,
        cohere_client_name=secrets.cohere_settings__client_name,
        cohere_model=secrets.cohere_settings__model_name,
    )
    extractor = MenuItemExtractor(llm_client=llm)
    pdf_converter = PdfChunker(
        pdf_path, model_weights_path=secrets.doclayout__model_path
    )  # TODO: chunker config
    pdf_pages = pdf_converter.chunk()

    menu_item_extraction_chunked = await asyncio.gather(
        *(extractor.extract(p) for p in pdf_pages), return_exceptions=True
    )

    menu_items: list[MenuItem] = []
    for extracted_menu_items in menu_item_extraction_chunked:
        if isinstance(extracted_menu_items, BaseException):
            logger.error("Error extracting menu items", exc_info=extracted_menu_items)
        else:
            menu_items.extend(extracted_menu_items)

    return Menu(service_charge=-1, menu_description="Missing", menu_items=menu_items)
