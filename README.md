# QRScanner Demo

A clean, modular Python project for generating and reading QR codes using a Tkinter-based GUI.

## Features

- Generate QR codes from Product Number and Serial Number input
- View the generated QR image
- Decode QR codes from saved images
- Simple GUI with clear structure
- SOLID-compliant code organization

## Tech Stack

- Python 3.11
- Tkinter (GUI)
- qrcode (QR generation)
- pyzbar + Pillow (QR decoding)

## Setup

To install dependencies:

    pip install -r requirements.txt

## Run

To launch the application:

    python main.py

## Project Structure

    qrscanner_demo/
    ├── main.py
    ├── assets/
    ├── services/
    ├── utils/
    └── ui/

## Notes

- The QR image is saved to `assets/sample_qr.png`
- Reading uses that same file for decoding preview

## License

MIT
