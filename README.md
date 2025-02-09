# Setup guide
Install following

- [tesseract](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0)
- [poppler](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0)

Add following to PATH
- `C:\Program Files\Tesseract-OCR`
- `C:\Program Files\poppler\bin`


Download [ara.traineddata](https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/ara.traineddata)

Copy `ara.traineddata` to `C:\Program Files\Tesseract-OCR\tessdata`

Now run following command

```
 pip install pdf2image pytesseract PyPDF2 pdfplumber opencv-python numpy
```

## Manual OCR
Download [gImageReader](https://github.com/manisandro/gImageReader/releases/download/v3.4.2/gImageReader_3.4.2_qt5_i686.exe)