import streamlit as st
import subprocess
import uuid
import os
from xhtml2pdf import pisa

st.title("📄 IPYNB to PDF Converter")

uploaded_file = st.file_uploader("Upload a `.ipynb` file", type="ipynb")

if uploaded_file:
    ipynb_filename = f"{uuid.uuid4()}.ipynb"
    html_filename = ipynb_filename.replace(".ipynb", ".html")
    pdf_filename = ipynb_filename.replace(".ipynb", ".pdf")

    with open(ipynb_filename, "wb") as f:
        f.write(uploaded_file.read())

    try:
        st.info("🔄 Converting notebook to HTML...")
        subprocess.run(["jupyter", "nbconvert", "--to", "html", ipynb_filename], check=True)

        st.info("📄 Converting HTML to PDF using xhtml2pdf...")

        with open(html_filename, "r", encoding="utf-8") as html_file:
            source_html = html_file.read()

        with open(pdf_filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(source_html, dest=pdf_file)

        if pisa_status.err:
            st.error("❌ PDF conversion failed.")
        else:
            with open(pdf_filename, "rb") as f:
                st.success("✅ Conversion complete!")
                st.download_button("⬇ Download PDF", f, file_name=pdf_filename)

    except Exception as e:
        st.error("❌ Conversion failed.")
        st.text(f"Details: {e}")

    finally:
        for f in [ipynb_filename, html_filename, pdf_filename]:
            if os.path.exists(f):
                os.remove(f)
