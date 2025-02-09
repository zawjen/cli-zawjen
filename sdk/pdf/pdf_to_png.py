import time
from pdf2image import convert_from_path
from sdk.pdf.pdf_converter import PdfConverter
from sdk.pdf.split_pdf import SplitPdf

class PdfToPng(PdfConverter):
    def __init__(self, pdf_path=None, dpi=200, folder_path=None, output_folder=None, split_pdf=True, output_extension="png"):
        super().__init__(pdf_path, dpi, folder_path, output_folder, split_pdf, output_extension)

    def convert(self, pdf_path):
        start_time = time.time()

        pages = convert_from_path(pdf_path, self.dpi)
        self.time_spent(f"Converted PDF to {self.output_extension} in", start_time)

        for idx, page in enumerate(pages, start=1):
            page_start = time.time()
            output_file_path = self.output_file_path(pdf_path)

            page.save(output_file_path, "PNG")
            self.time_spent(f"Saved page as {output_file_path} in", page_start)

    def convert_all(self, pdf_path):
        converter = PdfToPng(pdf_path=pdf_path, dpi=self.dpi, output_folder=self.output_folder, split_pdf=self.split_pdf)
        converter.convert_single_pdf()

