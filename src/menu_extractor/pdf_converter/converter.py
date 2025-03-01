from pathlib import Path

import pdfplumber


class PdfConverter:
    def __init__(self):
        pass

    def convert_to_text_pages(self, pdf_path: Path) -> list[str]:
        """Convert a pdf into a list of strings, with each string representing a page"""
        with pdfplumber.open(pdf_path) as pdf:
            pdf_contents = [p.extract_text(layout=True) for p in pdf.pages]
        return pdf_contents

    def convert_to_string(self, pdf_path: Path) -> str:
        pdf_pages = self.convert_to_text_pages(pdf_path)
        pdf_pages_as_str = "".join(
            [
                f"Page {index}.\nContent: {page_content}\n-----"
                for index, page_content in enumerate(pdf_pages, start=1)
            ]
        )
        return pdf_pages_as_str
