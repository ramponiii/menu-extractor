import asyncio
from pathlib import Path

from menu_extractor import logger, secrets
from menu_extractor.llm import LLM
from menu_extractor.models import (
    Menu,
    MenuItemList,
)
from menu_extractor.parsing import (
    parse_dict_str_from_llm_response,
)
from menu_extractor.pdf_converter import PdfConverter


class MenuExtractor:
    def __init__(self, pdf_converter: PdfConverter, llm: LLM):
        self.pdf_converter = pdf_converter
        self.llm = llm
        self.logger = logger

    async def extract_menu_from_pdf(self, pdf_path: Path) -> Menu:
        """Extracts the structured menu data from a PDF file."""
        try:
            self.logger.debug("Converting pdf pages to text")
            pdf_pages = self.pdf_converter.convert_to_text_pages(pdf_path)

            self.logger.debug("Extracting menu items")
            menu_items = await self._extract_menu_items_from_pages(pdf_pages)

            return Menu(
                menu_description="TODO", service_charge=-1, menu_items=menu_items
            )

        except Exception as e:
            self.logger.error(f"Error in menu extraction: {e}")
            raise

    async def _extract_menu_items_from_pages(
        self, pdf_pages: list[str]
    ) -> MenuItemList:
        """Extracts menu items from each page asynchronously."""
        llm_coros = [
            self.llm.extract_structured_data_string_from_menu_page(page)
            for page in pdf_pages
        ]
        responses = await asyncio.gather(*llm_coros)

        extracted_menu_items = [parse_dict_str_from_llm_response(r) for r in responses]

        merged_menu_items = MenuItemList(
            root=[
                item
                for menu_item_list in extracted_menu_items
                for item in menu_item_list.root
            ]
        )
        return merged_menu_items


async def main(pdf_path: Path) -> Menu:
    """The entry point to run the menu extraction process."""

    llm = LLM(
        cohere_api_key=secrets.cohere_settings__api_key,
        cohere_client_name=secrets.cohere_settings__client_name,
    )
    menu_extractor = MenuExtractor(pdf_converter=PdfConverter(), llm=llm)

    menu = await menu_extractor.extract_menu_from_pdf(pdf_path)

    return menu
