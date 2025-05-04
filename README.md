# [Live link]()

# 🩺 AI-Powered Prescription Extractor

Welcome to the **AI-Powered Prescription Extractor**, a Streamlit-based web app powered by **Groq’s Llama 3.1** and **Tesseract OCR**. It intelligently extracts and structures medical prescription data—perfect for doctors, pharmacists, medical staff, or patients needing clean and exportable prescription records.

---

## 🚀 Features

* 📸 **Supports Image Uploads**:
  * PNG
  * JPG
  * JPEG

* 🤖 **AI-Powered Structuring**:
  * Extracts **Patient Name**
  * Parses **Date** from prescriptions
  * Detects **Diagnosis** and **Medical Conditions**
  * Lists **Suggested Tests**
  * Extracts **Medications** (clean, comma-separated)
  * Identifies **Doctor's Name**

* 🔍 **Advanced Image Preprocessing**:
  * Enhances contrast & sharpens image before OCR
  * Uses Tesseract OCR for reliable text extraction

* 📄 **Export Options**:
  * Download structured data as **JSON**
  * Export prescription as a clean **PDF**

* ✨ **LangChain + Groq Integration**:
  * Uses **Llama 3.1-8b-instant** model via Groq API
  * Structured output using LangChain's `StructuredOutputParser`

---

## ⚙️ Tech Stack

* 🤖 `langchain`
* 🚀 `langchain_groq` (Llama 3.1 API)
* 🌐 `streamlit` for UI
* 🔠 `pytesseract` for OCR
* 🖼️ `Pillow` (Image preprocessing)
* 📄 `fpdf` for PDF export
* 🔐 `python-dotenv` for secure API key handling

---

## 📦 Installation

### 1. Clone the repository

```bash
https://github.com/vikas-kashyap97/Prescription-Extractor.git
cd Prescription-Extractor
```
### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install the required packages

```bash
pip install -r requirements.txt
```
### 4. Add your Google Generative AI API key

```bash
GROQ_API_KEY=your-google-api-key-here
```
### 5. Run the application

```bash
streamlit run prompt_ui.py
```

## On the UI:

- Upload an image of a medical prescription (PNG, JPG, JPEG).
- View the raw OCR-extracted text.
- Click "Structure with Llama-3.1 (Groq)" to extract structured fields.
- See the cleanly displayed prescription details.
- Export the extracted data as JSON or PDF with a click.

## Acknowledgements

- LangChain
- Streamlit
- Groq Llama 3.1
- Tesseract OCR
- Pillow
- FPDF

## 📄 License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
