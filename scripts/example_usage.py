import asyncio
from pathlib import Path

from menu_extractor import logger
from menu_extractor.run import pdf_to_menu

menu = asyncio.run(pdf_to_menu(pdf_path=Path("tests/data/ronis.pdf")))

logger.info("Writing to example_output_ronis.json ...")

with open("example_output_ronis.json", "w") as file:
    file.write(menu.model_dump_json(indent=4))
