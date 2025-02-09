import os
from PyPDF2 import PdfReader, PdfWriter
import time

class SplitPdf:
    def __init__(self, pdf_path, output_folder=None, pages_per_split=1):
        """
        Initialize the PDF splitter.

        :param pdf_path: Path to the input PDF file.
        :param output_folder: Folder to save the split PDFs.
        :param pages_per_split: Number of pages per split PDF.
        """
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.pages_per_split = pages_per_split

        if not self.output_folder:
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
            self.output_folder = os.path.join(os.path.dirname(self.pdf_path), "out", base_name, "pdf")
            os.makedirs(self.output_folder, exist_ok=True)

    def time_spent(self, message, start_time):
        """
        Print the time spent for an operation.

        :param message: Message to display.
        :param start_time: Start time of the operation.
        """
        spent = time.time() - start_time
        print(f"{message} {spent:.2f} seconds.")

    def split(self):
        """
        Splits the PDF into smaller PDFs.
        :return: List of paths to the split PDFs.
        """
        try:
            start_time = time.time()

            # Ensure output folder exists
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
                print(f"Created output folder: {self.output_folder}")

            print(f"Reading PDF: {self.pdf_path}")
            pdf_reader = PdfReader(self.pdf_path)
            total_pages = len(pdf_reader.pages)
            print(f"Total pages in PDF: {total_pages}")

            split_pdf_paths = []

            for start_page in range(0, total_pages, self.pages_per_split):
                writer = PdfWriter()
                end_page = min(start_page + self.pages_per_split, total_pages)
    
                for page_num in range(start_page, end_page):
                    writer.add_page(pdf_reader.pages[page_num])

                split_pdf_name = f"{os.path.splitext(os.path.basename(self.pdf_path))[0]}_{start_page + 1}"

                if self.pages_per_split == 1:
                    split_pdf_name += f".pdf"
                else:
                    split_pdf_name += f"_{end_page}.pdf"

                split_pdf_path = os.path.join(self.output_folder, split_pdf_name)

                try:
                    with open(split_pdf_path, 'wb') as split_pdf_file:
                        writer.write(split_pdf_file)
                    print(f"Saved split {start_page + 1} to {end_page} of PDF: {split_pdf_path}")
                    split_pdf_paths.append(split_pdf_path)
                except Exception as e:
                    print(f"Error saving split PDF '{split_pdf_name}': {e}")

            self.time_spent(f"Successfully split PDF into {len(split_pdf_paths)} parts in ", start_time)
         
            return split_pdf_paths

        except FileNotFoundError:
            print(f"Error: File '{self.pdf_path}' not found.")
            return []
        except PermissionError:
            print(f"Error: Permission denied for file '{self.pdf_path}'.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
