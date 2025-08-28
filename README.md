


# 🧾 Invoice OCR Extraction (Flask + Tesseract)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-Framework-green)](https://flask.palletsprojects.com/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A web application for extracting **structured data from invoices** using **Flask, Python, and Tesseract OCR**.  
The app supports both **images and PDFs**, detects invoice details, and outputs clean tabular data.

---

## ✨ Features
- 📤 Upload **PDF or image invoices**  
- 🔍 Extract key details:
  - Invoice Number  
  - Date  
  - Items (Description + Amount)  
- 📑 Works with **multi-page PDFs**  
- 🧹 Cleans noisy OCR results (removes extra headers like `Description Amount`)  
- 💾 Export results to **Excel (xlsx)** 

---

## 🚀 Applications

This project can be used in:

- **Accounting & Finance** → Automating invoice data entry and reconciliation.  
- **ERP / CRM Systems** → Feeding structured invoice data directly into enterprise workflows.  
- **Document Management** → Organizing scanned invoices into searchable digital records.  
- **Auditing & Compliance** → Extracting structured data for financial reviews and tax compliance.  
- **SMEs & Startups** → Reducing manual effort in handling supplier invoices.  


## 📂 Project Structure

├── app.py # Flask application
├── templates/
 └── index.html # Frontend upload & results page

## ⚙️ Installation

### Install Tesseract OCR

This project uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction.  
Please install it based on your operating system:

- **Windows**: [Download the Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)  
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr


## 🖼️ Usage
1. Run the Flask app:
   ```bash
   python app.py
2.Open your browser and go to:http://127.0.0.1:5000/
3. Upload a PDF or image of an invoice.  
4. Click **Extract**.  
5. View extracted details:
   - Invoice Number  
   - Date  
   - Description & Amount table  
6. Optionally download results as **Excel**  

---

## 📦 Requirements

- Python 3.8+  
- [Flask](https://flask.palletsprojects.com/)  
- [pytesseract](https://pypi.org/project/pytesseract/)  
- [pdf2image](https://pypi.org/project/pdf2image/)  
- [pandas](https://pypi.org/project/pandas/)  
- [Pillow](https://pypi.org/project/Pillow/)  
