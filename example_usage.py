import asyncio
from pathlib import Path

from menu_extractor import logger
from menu_extractor.main import main

menu = asyncio.run(main(pdf_path=Path("tests/data/garden_gate.pdf")))

logger.info("Writing to output.txt ...")
with open("output.txt", "w") as file:
    file.write(menu.model_dump_json(indent=4))
