from pathlib import Path

import pdfplumber
from doclayout_yolo import YOLOv10
from pdf2image import convert_from_path


class PdfChunker:
    def __init__(self, pdf_path: Path, model_weights_path: str):
        self._pdf_path = pdf_path
        self._doclayout_model = YOLOv10(model_weights_path)

    def chunk(self) -> list[str]:
        pages = self._pdf_to_images()
        chunks = []
        for page_num, page_image in enumerate(pages):
            detected_chunks = self._identify_text_chunks(page_image)
            print(f"Detected Chunks on page {page_num}: {detected_chunks}")

            for chunk in detected_chunks:
                # Assuming chunk is a tuple of (normalized_x_center, normalized_y_center, width, height)
                text = self._extract_text_from_bounding_box(page_num, chunk)
                if text:
                    chunks.append(text)
        return chunks

    def _pdf_to_images(self):
        """Convert the PDF to images for YOLO to process."""
        return convert_from_path(self._pdf_path)

    def _identify_text_chunks(self, page_image):
        """Run the YOLOv10 model on the image and return the detected text chunks."""
        detection_result = self._doclayout_model.predict(
            [page_image], imgsz=1024, conf=0.2, device="cpu"
        )

        boxes = detection_result[0].boxes
        detected_chunks = []
        for box in boxes:
            # Extract the normalized bounding box from the detection result (xywhn)
            box_data = box.xywhn[
                0
            ]  # xywhn is normalized [x_center, y_center, width, height]
            detected_chunks.append(tuple(map(float, box_data)))

        return detected_chunks

    def _extract_text_from_bounding_box(
        self, page_num: int, bbox_normalized: tuple[float, float, float, float]
    ) -> str:
        """Extract text from a bounding box on the PDF page."""
        with pdfplumber.open(self._pdf_path) as pdf:
            page = pdf.pages[page_num]
            page_width, page_height = page.width, page.height

            # Convert normalized coordinates to actual pixel coordinates
            x_center, y_center, width, height = bbox_normalized
            x1 = (x_center - width / 2) * page_width
            y1 = (y_center - height / 2) * page_height
            x2 = (x_center + width / 2) * page_width
            y2 = (y_center + height / 2) * page_height

            bbox = (x1, y1, x2, y2)

            # Crop the page and extract text from the bounding box
            cropped_page = page.within_bbox(bbox)
            return cropped_page.extract_text() if cropped_page else None


if __name__ == "__main__":
    weights = "sandbox/layout.pt"  # Path to the YOLO model weights
    pdf = "tests/data/ronis.pdf"  # Path to the input PDF file

    chunker = PdfChunker(pdf, weights)
    chunks = chunker.chunk()

    print(f"Extracted Text Chunks: {chunks}")
