# Setup guide
This is a setup guide for zac or Zawjen CLI (Command Line Interface). 

## Install Software
Install following

- [tesseract](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0)
- [poppler](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0)
- [gImageReader](https://github.com/manisandro/gImageReader/releases/download/v3.4.2/gImageReader_3.4.2_qt5_i686.exe)

## Setup Path
Add following to PATH
- `C:\Program Files\Tesseract-OCR`
- `C:\Program Files\poppler\bin`

## Copy Arabic Package
Download [ara.traineddata](https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/ara.traineddata)

Copy `ara.traineddata` to `C:\Program Files\Tesseract-OCR\tessdata`

## Install Python
Install Python 3.13.0. Check your current python version using following command:

```
py -V
```

```
python -V
```

## Install Packages
Run following `pip` command to install required packages:

```
 pip install pdf2image pytesseract PyPDF2 pdfplumber opencv-python numpy
```

## Run Zac
Run following command to run zac:

```
py main.py
```