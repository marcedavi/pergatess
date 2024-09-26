# pergatess
Software that uses Tesseract to review some documents for typos.

## Disclaimer
You can expect ~15 minutes of processing time (pdf2image + inference) for a ~270 pages PDF but it depends on your CPU.
Splitting a PDF into images seems to be awfully slow using the most popular library pdf2image.
On Windows the UI dimensions are a bit off (some elements are shorter than they should be/they are on Linux).

## Preparation
You should have a folder that contains only the Excel files and another folder that contains only the PDF files.
Each Excel file name should be the same as the corresponding PDF file name.
The Excel extension can be xlsx, xls, xlsm and a few more, the software should work fine regardless.

For example:
~/excels
|___ 1.xlsx
|___ 2.xlsx
|___ 3.xlsx

~/pdfs
|___ 1.pdf
|___ 2.pdf
|___ 3.pdf

## Setup
The software works on both linux and windows.

You need to install Tesseract 5 binaries for your OS and it to the system PATH.
On Windows i recommend the unofficial installers from UB Mannheim.
You can find everything here:
https://tesseract-ocr.github.io/tessdoc/Downloads.html

- git clone https://github.com/marcedavi/pergatess
- cd pergatess
- python -m pip install -r requirements.txt
- python main.py

## How to use
After you run the program the main window should open.

- Select the folder that contains the Excel files
- Select the folder that contains the PDF files
- Click "Rileva errori"
