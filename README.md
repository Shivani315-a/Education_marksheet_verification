# 🎓 Marksheet Verification System

OCR-based academic marksheet verification system built using:

- Streamlit
- EasyOCR
- RapidFuzz
- PyMuPDF

## 🚀 Features

- PDF to OCR extraction (No Tesseract, No Poppler)
- Name and surname fuzzy matching
- Education level detection
- Pass/Fail detection
- Clean UI

## 📦 Installation

pip install -r requirements.txt

## ▶ Run

streamlit run app.py

## 📌 Project Structure

app.py → Streamlit UI  
ocr_utils.py → OCR extraction  
verification.py → Verification logic  
