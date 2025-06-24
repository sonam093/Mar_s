
    import streamlit as st
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDF
import docx2txt


# ---- TEXT EXTRACTION FUNCTIONS ----

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(uploaded_file):
    return docx2txt.process(uploaded_file)

def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")

def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)


# ---- METADATA GENERATION ----

def generate_metadata(text, filename):
    return {
        "filename": filename,
        "word_count": len(text.split()),
        "character_count": len(text),
        "summary": text[:300] + "..." if len(text) > 300 else text,
        "keywords": list(set(text.lower().split()))[:10]
    }    

# ---- STREAMLIT UI ----

st.set_page_config(page_title="Metadata Generator", layout="centered")
st.title("📄 Automated Metadata Generator")
st.write("Upload a PDF, DOCX, TXT, or Image file to extract metadata.")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    file_name = uploaded_file.name
    ext = file_name.split('.')[-1].lower()

    st.info(f"Processing `{file_name}` ...")

    try:
        if ext == 'pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif ext == 'docx':
            text = extract_text_from_docx(uploaded_file)
        elif ext == 'txt':
            text = extract_text_from_txt(uploaded_file)
        elif ext in ['png', 'jpg', 'jpeg']:
            text = extract_text_from_image(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()

        st.success("✅ Text extracted successfully!")
        st.subheader("📃 Extracted Text (first 1000 characters)")
        st.text_area("Text Preview", text[:1000], height=250)

        if st.button("Generate Metadata"):
            with st.spinner("Generating metadata..."):
                metadata = generate_metadata(text, file_name)
                st.subheader("📑 Generated Metadata")
                st.json(metadata)

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
