# Pergatess
University project that involved the fine-tuning of Tesseract to detect typos in degree certificates.

## Preparation
The Excel and PDF files can be either in a single folder or in two separate folders.
What's important is that in such folder(s) there aren't any unnecessary PDF or Excel files because the software looks for any file with ".pdf" or ".xls*" extension so it will pick up the wrong files as well.
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

## Compilation
If you need to produce a standalone executable for Windows follow this steps:

- git clone https://github.com/marcedavi/pergatess
- cd pergatess
- python -m pip install -r requirements.txt
- python -m PyInstaller --onefile --windowed --add-data "dependencies;dependencies" .\main.py

You will find the executable under the "dist" directory.

## Setup
The software works on both linux and windows.

You need to install Tesseract 5 binaries for your OS and add it to the system PATH.
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
