# Image_based-invoice_and-form-filler-agent


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
- 💾 Export results to **Excel (xlsx)** or **JSON**

---

## 📂 Project Structure

