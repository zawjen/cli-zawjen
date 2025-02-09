import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os
import re
import logging
from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np
from pdf2image import convert_from_path

# Initialize logger
logging.basicConfig(level=logging.INFO)

class PDFSectionExtractor:
    def __init__(self, pdf_path, num_vertical=1, num_horizontal=1, use_ocr=True, ocr_resolution=300):
        """
        Initialize the extractor with the PDF path and section settings.
        :param pdf_path: Path to the input PDF file.
        :param num_vertical: Number of vertical sections (columns).
        :param num_horizontal: Number of horizontal sections (rows).
        :param use_ocr: If True, use OCR for scanned PDFs.
        :param ocr_resolution: DPI resolution for OCR processing.
        """
        self.pdf_path = pdf_path
        self.num_vertical = num_vertical
        self.num_horizontal = num_horizontal
        self.use_ocr = use_ocr
        self.ocr_resolution = ocr_resolution
        self.base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    def extract_text_from_sections(self):
        """
        Extract text from multiple sections in a PDF.
        Saves each section in a separate text file and annotated image.
        """
        pages = convert_from_path(self.pdf_path, dpi=self.ocr_resolution)  # Convert PDF pages to images
        for page_num, pil_image in enumerate(pages, start=1):
            width, height = pil_image.size

            # If only one vertical section and one horizontal section, extract the whole page
            if self.num_vertical == 1 and self.num_horizontal == 1:
                text, annotated_image = self.extract_text_using_ocr(pil_image, resolution=self.ocr_resolution)
                self.save_section_image(annotated_image, page_num, 0, 0)
                self.save_section_text(text, page_num, 0, 0)
                continue

            section_width = width / self.num_vertical
            section_height = height / self.num_horizontal

            with ThreadPoolExecutor() as executor:
                futures = []
                for row in range(self.num_horizontal):
                    for col in range(self.num_vertical):
                        left = col * section_width
                        top = row * section_height
                        right = (col + 1) * section_width
                        bottom = (row + 1) * section_height
                        bbox = (left, top, right, bottom)

                        futures.append(executor.submit(self.process_section, pil_image, bbox, page_num, row, col))

                for future in futures:
                    future.result()
    
    def process_section(self, pil_image, bbox, page_num, row, col):
        """
        Process a single section of the page for text extraction and OCR.
        """
        try:
            # Log bbox for debugging
            logging.info(f"Processing section {page_num}, section {row}_{col}, bbox: {bbox}")

            cropped_image = pil_image.crop(bbox)
            section_text, annotated_image = self.extract_text_using_ocr(cropped_image)

            self.save_section_image(annotated_image, page_num, row, col)
            self.save_section_text(section_text, page_num, row, col)
        except Exception as e:
            logging.error(f"Error processing page {page_num}, section {row}_{col}: {e}")

    def extract_text_using_ocr(self, image, resolution=300):
        """
        Extracts text using OCR with enhanced preprocessing.
        :param image: PIL image object.
        :param resolution: Resolution for OCR processing.
        :return: Extracted text and annotated image.
        """
        logging.info(f"Processing image with resolution: {resolution}")

        # Preprocessing: Adaptive binarization & denoising
        preprocessed_image = self.preprocess_image(image)

        # OCR processing with adaptive PSM and OEM options
        ocr_data = pytesseract.image_to_data(
            preprocessed_image, lang="ara", config="--psm 1 --oem 3", output_type=pytesseract.Output.DICT
        )

        # Annotate detected text areas
        annotated_image = self.draw_text_boxes(preprocessed_image, ocr_data)

        # Extracted text
        extracted_text = "\n".join(ocr_data["text"]).strip()

        return extracted_text, annotated_image

    def preprocess_image(self, image):
        """
        Apply preprocessing to enhance OCR accuracy (i2OCR-style).
        :param image: PIL image object.
        :return: Preprocessed image.
        """
        # Convert to grayscale using PIL
        image = image.convert("L")

        # Convert PIL image to OpenCV format for further processing
        open_cv_image = np.array(image)

        # Gaussian blur
        blur = cv2.GaussianBlur(open_cv_image, (3, 3), 0)

        # Otsu's thresholding
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Morphological operation (remove noise)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Invert image
        invert = 255 - opening

        # Convert back to PIL for compatibility with pytesseract
        preprocessed_image = Image.fromarray(invert)

        return preprocessed_image

    def draw_text_boxes(self, image, ocr_data):
        """
        Draw green bounding boxes around detected text areas.
        :param image: PIL image object.
        :param ocr_data: OCR detection data.
        :return: Annotated PIL image.
        """
        # Convert image to RGB to ensure drawing works
        image = image.convert("RGB")

        draw = ImageDraw.Draw(image)

        for i in range(len(ocr_data["text"])):  
            if ocr_data["text"][i].strip():  # Ignore empty text detections
                x, y, w, h = (
                    ocr_data["left"][i],
                    ocr_data["top"][i],
                    ocr_data["width"][i],
                    ocr_data["height"][i],
                )
                draw.rectangle([x, y, x + w, y + h], outline="green", width=2)

        return image

    def save_section_text(self, text, page_num, row, col):
        """
        Save the extracted text to a separate file.
        :param text: Extracted text.
        :param page_num: Page number.
        :param row: Row index.
        :param col: Column index.
        """
        section_filename = f"{self.base_filename}_page{page_num}_section{row}_{col}.txt"
        with open(section_filename, "w", encoding="utf-8") as file:
            file.write(text)

    def save_section_image(self, image, page_num, row, col):
        """
        Save the annotated section image with green OCR boxes.
        :param image: Annotated PIL image.
        :param page_num: Page number.
        :param row: Row index.
        :param col: Column index.
        """
        section_filename = f"{self.base_filename}_page{page_num}_section{row}_{col}.png"
        image.save(section_filename)

# Example Usage:
# extractor = PDFSectionExtractor("example.pdf", num_vertical=2, num_horizontal=1, use_ocr=True, ocr_resolution=300)
# extractor.extract_text_from_sections()
