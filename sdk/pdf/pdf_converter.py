import os
import time
from pdf2image import convert_from_path
from sdk.pdf.split_pdf import SplitPdf

class PdfConverter:
    def __init__(self, pdf_path=None, dpi=200, folder_path=None, output_folder=None, split_pdf=True, output_extension=None):
        """
        Initialize the converter with paths and settings.

        :param pdf_path: Path to the input PDF file (optional).
        :param dpi: Resolution for converting PDF to images.
        :param folder_path: Path to a folder containing PDF files (optional).
        :param output_folder: Folder to save PNG images (optional).
        :param split_pdf: Whether to split the PDF into smaller parts before processing.
        """
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.folder_path = folder_path
        self.split_pdf = split_pdf
        self.output_extension = output_extension
        self.output_folder = output_folder

        if not self.output_folder:
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
            self.output_folder = os.path.join(os.path.dirname(self.pdf_path), "out", base_name)
            os.makedirs(self.output_folder, exist_ok=True)

    def time_spent(self, message, start_time):
        """
        Print the time spent for an operation.

        :param message: Message to display.
        :param start_time: Start time of the operation.
        """
        spent = time.time() - start_time
        print(f"[{spent:.2f}s] {message}")

    def convert_single_pdf(self):
        """
        Converts a single PDF and saves them to the output folder.
        """
        if not self.pdf_path:
            print("Error: No PDF file specified.")
            return

        try:
            start_time = time.time()
            if self.split_pdf:
                split_pdfs = self.split()

                for split_pdf in split_pdfs:
                    self.extract_from_pdf(split_pdf)
            else:
                self.extract_from_pdf(self.pdf_path)

            self.time_spent(f"Conversion completed: {self.pdf_path}", start_time)
        except Exception as e:
            print(f"An error occurred while processing '{self.pdf_path}': {e}")

    def split(self):
        """
        Split the PDF into smaller parts.
        :return: List of paths to the split PDFs.
        """

        splitter = SplitPdf(self.pdf_path)

        print(f"Starting PDF splitting: {self.pdf_path}")
        start_time = time.time()
        split_pdfs = splitter.split()
        self.time_spent(f"PDF splitting completed: {self.pdf_path}", start_time)

        return split_pdfs

    def extract_from_pdf(self, pdf_path):
        """
        Extracts PNG images from a single PDF file.
        :param pdf_path: Path to the PDF file.
        """
        try:
            self.convert(pdf_path)

        except Exception as e:
            print(f"An error occurred during {self.output_extension} extraction: {e}")

    def convert(self, pdf_path):
        pass

    def output_file_path(self, pdf_path):
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        ext_folder = os.path.join(self.output_folder, self.output_extension)
        os.makedirs(ext_folder, exist_ok=True)
        output_file_path = os.path.join(self.output_folder, self.output_extension, f"{base_name}.{self.output_extension}")

        return output_file_path

    def convert_all_pdfs_in_folder(self):
        """
        Converts all PDFs in the specified folder to PNG images.
        """
        if not self.folder_path:
            print("Error: No folder specified.")
            return

        if not os.path.isdir(self.folder_path):
            print(f"Error: The folder '{self.folder_path}' does not exist.")
            return

        # Get all PDF files in the folder
        pdf_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print(f"No PDF files found in folder '{self.folder_path}'.")
            return

        print(f"Found {len(pdf_files)} PDF(s) in '{self.folder_path}'.")
        total_start_time = time.time()
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.folder_path, pdf_file)

            # Create a new instance for each PDF file
            self.convert_all(pdf_path)

        self.time_spent(f"All PDFs in folder processed: {self.folder_path}", total_start_time)

    def convert_all(self, pdf_path):
        pass

    def start(self):
        """
        Main method to perform conversion. Decides based on provided paths.
        """
        if self.pdf_path:
            self.convert_single_pdf()
        elif self.folder_path:
            self.convert_all_pdfs_in_folder()
        else:
            print("Error: Either a PDF file or a folder containing PDFs must be specified.")
