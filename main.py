from sdk.img.img_to_text import ImageToTextConverter
from sdk.pdf.pdf_section_extractor import PDFSectionExtractor
from sdk.pdf.pdf_to_text import PdfToText
from sdk.pdf.pdf_to_png import PdfToPng

def main():
    # Convert a single PDF file
    single_pdf_path = r"C:\data\code\pdf-cli\test\data\2-col.pdf"  # Replace with your PDF file path

    # Convert all PDFs in a folder
    folder_path = r"C:\data\books\dictionary\Lisan ul Arab"  # Replace with your folder path containing PDFs

    # Uncomment one of the options below based on your needs:

    # Option 1: Convert a single PDF file
    # converter = PdfToText(pdf_path=single_pdf_path, split_pdf=True)
    # converter.start()

    # Option 2: Convert all PDFs in a folder
    #converter = PdfToText(folder_path=folder_path)
    #converter.start()

    # converter = PdfToPng(pdf_path=single_pdf_path, dpi=300)
    # converter.start()

    # Create an instance of PDFColumnExtractor
    # extractor = PDFSectionExtractor(single_pdf_path, num_vertical=1, num_horizontal=1)
    # column_texts = extractor.extract_text_from_sections()

    converter = ImageToTextConverter()  # Initialize the converter
    text = converter.convert_image_to_text(r"C:\data\code\pdf-cli\test\data\page-001.png")  # Provide the image path
    print(text)  # Print the extracted text
    
    # Print extracted Arabic text
    # for i, (right_text, left_text) in enumerate(column_texts, start=1):
    #     print(f"Page {i}:")
    #     print("Right Column (Arabic Primary):\n", right_text)
    #     print("Left Column:\n", left_text)
    #     print("=" * 50)

if __name__ == "__main__":
    main()
