import pytesseract
from pdf2image import convert_from_path
import time
from sdk.pdf.pdf_converter import PdfConverter
from sdk.pdf.split_pdf import SplitPdf

class PdfToText(PdfConverter):
    def __init__(self, pdf_path=None, dpi=200, folder_path=None, output_folder=None, split_pdf=True, output_extension="txt"):
        super().__init__(pdf_path, dpi, folder_path, output_folder, split_pdf, output_extension)

    def convert(self, pdf_path):
        start_time = time.time()
    
        text_data = ''

        # Convert PDF pages to images
        pages = convert_from_path(pdf_path, self.dpi, thread_count=1, grayscale=False)
        self.time_spent(f"Converted to image list: {pdf_path}", start_time)

        page_no = 1
        for page in pages:
            page_start = time.time()
            text_data += pytesseract.image_to_string(page, lang='ara') + '\n'
            self.time_spent(f"Extracted text from page {page_no}: {pdf_path}", page_start)
            page_no += 1

        # Save the text to the output file
        output_file_path = self.output_file_path(pdf_path)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text_data)

        self.time_spent(f"Saved file: {output_file_path}", start_time)

    def convert_all(self, pdf_path):
        converter = PdfToText(pdf_path=pdf_path, dpi=self.dpi, split_pdf=self.split_pdf)
        converter.convert_single_pdf()