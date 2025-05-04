import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import json
from io import BytesIO
from fpdf import FPDF
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# ✅ Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ✅ Load .env variables
load_dotenv()

# ✅ Initialize Groq Llama 3.1-8b-instant
model = ChatGroq(model="llama-3.1-8b-instant")

# ✅ Define output structure
response_schemas = [
    ResponseSchema(name="patient_name", description="Full name of the patient"),
    ResponseSchema(name="date", description="Date mentioned in the prescription"),
    ResponseSchema(name="diagnosis", description="Diagnosis or medical condition"),
    ResponseSchema(name="tests_suggested", description="Medical tests suggested"),
    ResponseSchema(name="medications", description="Medicines prescribed, always as a single comma-separated string"),
    ResponseSchema(name="doctor_name", description="Doctor's name"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# ✅ LangChain cleaning function with safe error handling
def clean_and_structure(raw_text):
    prompt = ChatPromptTemplate.from_template(
        """You are a medical transcription AI assistant.
Extract and structure the following information from this raw OCR text.
{format_instructions}

OCR text:
{raw_text}
"""
    )
    chain = prompt | model | output_parser
    try:
        return chain.invoke({"raw_text": raw_text, "format_instructions": format_instructions})
    except Exception as e:
        st.error(f"❌ Failed to parse structured output. Error: {e}")
        return {
            "patient_name": "N/A",
            "date": "N/A",
            "diagnosis": "N/A",
            "tests_suggested": "N/A",
            "medications": "N/A",
            "doctor_name": "N/A",
        }

# ✅ Preprocess image before OCR
def preprocess_image(image):
    image = image.convert('L')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    image = image.filter(ImageFilter.SHARPEN)
    return image

# ✅ PDF Export Function (without emojis)
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Prescription Details", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Patient Name: {data.get('patient_name', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {data.get('date', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Doctor: {data.get('doctor_name', 'N/A')}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Diagnosis:", ln=True)
    pdf.multi_cell(0, 10, data.get('diagnosis', 'N/A'))
    pdf.ln(5)

    pdf.cell(200, 10, txt="Tests Suggested:", ln=True)
    pdf.multi_cell(0, 10, data.get('tests_suggested', 'N/A'))
    pdf.ln(5)

    pdf.cell(200, 10, txt="Medications:", ln=True)
    meds = data.get('medications', 'N/A')
    if meds != 'N/A':
        for med in meds.replace('\n', ',').split(','):
            pdf.cell(200, 10, txt=f"  - {med.strip()}", ln=True)
    else:
        pdf.multi_cell(0, 10, 'N/A')

    return pdf.output(dest='S').encode('latin1')

# ✅ Clean Streamlit display function
def display_structured_output(data):
    st.success(f"👤 Patient Name: {data.get('patient_name', 'N/A')}")
    st.info(f"🗓️ Date: {data.get('date', 'N/A')}")
    st.markdown("---")

    st.subheader("🩺 Diagnosis")
    st.write(data.get('diagnosis', 'N/A'))

    st.subheader("🧪 Tests Suggested")
    st.write(data.get('tests_suggested', 'N/A'))

    st.subheader("💊 Medications")
    meds = data.get('medications', 'N/A')
    if meds != 'N/A':
        meds_list = [m.strip() for m in meds.replace('\n', ',').split(',') if m.strip()]
        for med in meds_list:
            st.markdown(f"- {med}")
    else:
        st.write("N/A")

    st.markdown("---")
    st.success(f"👨‍⚕️ Doctor: {data.get('doctor_name', 'N/A')}")

    # ✅ Export Buttons
    st.markdown("### 📦 Export Options")
    json_data = json.dumps(data, indent=2)
    st.download_button("⬇️ Download JSON", json_data, file_name="prescription.json", mime="application/json")

    pdf_bytes = generate_pdf(data)
    st.download_button("⬇️ Download PDF", pdf_bytes, file_name="prescription.pdf", mime="application/pdf")

# ✅ Streamlit UI
st.title("🩺 Prescription Extractor (Llama 3.1 + Tesseract + Export)")

uploaded_file = st.file_uploader("📤 Upload Prescription Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='📸 Uploaded Prescription', use_column_width=True)
    
    # OCR Step
    with st.spinner('🔍 Running OCR with Tesseract...'):
        processed_image = preprocess_image(image)
        raw_text = pytesseract.image_to_string(processed_image)
    
    st.subheader("📄 Raw OCR Text:")
    st.text_area("OCR Output", raw_text, height=200)

    # Structure button
    if st.button("Structure with Llama-3.1 (Groq)"):
        with st.spinner('Extracting structured fields...'):
            structured_output = clean_and_structure(raw_text)
        st.subheader("✅ Extracted Prescription Details:")
        display_structured_output(structured_output)
