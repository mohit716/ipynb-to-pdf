import streamlit as st
import subprocess
import uuid
import os
import pdfkit

st.title("📄 IPYNB to PDF Converter")

uploaded_file = st.file_uploader("Upload a `.ipynb` file", type="ipynb")

if uploaded_file:
    input_ipynb = f"{uuid.uuid4()}.ipynb"
    input_html = input_ipynb.replace(".ipynb", ".html")
    output_pdf = input_ipynb.replace(".ipynb", ".pdf")

    with open(input_ipynb, "wb") as f:
        f.write(uploaded_file.read())

    try:
        st.info("🔄 Converting notebook to HTML...")
        subprocess.run(["jupyter", "nbconvert", "--to", "html", input_ipynb], check=True)

        st.info("📄 Converting HTML to PDF...")
        pdfkit.from_file(input_html, output_pdf)

        with open(output_pdf, "rb") as f:
            st.success("✅ Conversion complete!")
            st.download_button("⬇ Download PDF", f, file_name=output_pdf)

    except Exception as e:
        st.error("❌ Conversion failed.")
        st.text(f"Details: {e}")

    finally:
        for f in [input_ipynb, input_html, output_pdf]:
            if os.path.exists(f):
                os.remove(f)
