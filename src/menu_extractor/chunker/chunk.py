from pathlib import Path

import pdfplumber

from menu_extractor import logger


class PdfChunker:
    def __init__(self, pdf_path: Path):
        logger.info("Loading Chunking model...")
        self._pdf = pdfplumber.open(pdf_path)

    def chunk(self) -> list[str]:
        chunks = [p.extract_text() for p in self._pdf.pages]
        print(chunks)
        exit()
        logger.info("Produced text chunks from pdf", extra={"n_chunks": len(chunks)})
        return chunks
