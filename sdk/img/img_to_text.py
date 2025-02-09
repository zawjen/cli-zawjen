from PIL import Image, ImageDraw
import pytesseract
import os

class ImageToTextConverter:
    def __init__(self, tesseract_path=None):
        """
        Initialize the ImageToTextConverter.
        :param tesseract_path: Path to the Tesseract executable if it's not in the PATH.
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def convert_image_to_text(self, image_path, lang="ara"):
        """
        Convert an image to text using Tesseract OCR with support for Arabic.
        :param image_path: Path to the image file.
        :param lang: Language code for OCR (default is "ara" for Arabic).
        :return: Extracted text.
        """
        try:
            # Open the image file using Pillow
            image = Image.open(image_path)

            # Extract text from image using pytesseract
            text = pytesseract.image_to_string(image, lang=lang)

            # Get detailed OCR data (text and bounding boxes)
            ocr_data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)

            # Annotate the image by drawing green rectangles around detected text
            annotated_image = self.annotate_image(image, ocr_data)

            # Generate the annotated image path with original extension and "_ocr" suffix
            base_name, ext = os.path.splitext(image_path)  # Split the extension
            annotated_image_path = f"{base_name}_ocr{ext}"  # Append _ocr to the base name

            # Save the annotated image
            annotated_image.save(annotated_image_path)

            return text, annotated_image_path

        except Exception as e:
            print(f"Error processing image: {e}")
            return None, None

    def annotate_image(self, image, ocr_data):
        """
        Annotate the image with green rectangles around detected text.
        :param image: PIL image object.
        :param ocr_data: OCR data with bounding box information.
        :return: Annotated PIL image.
        """
        # Convert the image to RGB to ensure we can draw on it
        image = image.convert("RGB")

        # Create a drawing context on the image
        draw = ImageDraw.Draw(image)

        # Loop through each word in the OCR data and draw a rectangle around it
        for i in range(len(ocr_data["text"])):
            text = ocr_data["text"][i]
            if text.strip():  # Only consider non-empty text
                # Get the coordinates for the bounding box
                x, y, w, h = ocr_data["left"][i], ocr_data["top"][i], ocr_data["width"][i], ocr_data["height"][i]
                draw.rectangle([x, y, x + w, y + h], outline="green", width=2)

        return image

