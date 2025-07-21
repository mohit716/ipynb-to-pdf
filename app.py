import streamlit as st
import subprocess
import uuid
import os

st.title("📄 IPYNB to PDF Converter")

uploaded_file = st.file_uploader("Upload a `.ipynb` file", type="ipynb")

if uploaded_file:
    input_filename = f"{uuid.uuid4()}.ipynb"
    with open(input_filename, "wb") as f:
        f.write(uploaded_file.read())

    output_filename = input_filename.replace(".ipynb", ".pdf")

    try:
        st.info("🔄 Converting to PDF using LaTeX...")
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "pdf", input_filename],
            check=True
        )
        with open(output_filename, "rb") as f:
            st.success("✅ Conversion complete!")
            st.download_button("⬇ Download PDF", f, file_name=output_filename)
    except subprocess.CalledProcessError as e:
        st.error("❌ Conversion failed. This may happen if LaTeX is not available.")
        st.text(f"Error details: {e}")
    finally:
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)
