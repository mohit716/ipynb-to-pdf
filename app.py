import streamlit as st
import subprocess
import uuid
import os

st.title("📄 IPYNB to PDF Converter")

uploaded_file = st.file_uploader("Upload a `.ipynb` file", type="ipynb")

if uploaded_file:
    # Save the uploaded file with a random name
    input_filename = f"{uuid.uuid4()}.ipynb"
    with open(input_filename, "wb") as f:
        f.write(uploaded_file.read())

    # Define the output filename
    output_filename = input_filename.replace(".ipynb", ".pdf")

    try:
        st.info("🚀 Converting to PDF (using webpdf)...")
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "webpdf", "--allow-chromium-download", input_filename],
            check=True
        )
        # Show download button
        with open(output_filename, "rb") as f:
            st.success("✅ Conversion complete!")
            st.download_button("⬇️ Download PDF", f, file_name="converted_notebook.pdf")
    except Exception as e:
        st.error(f"❌ Conversion failed: {str(e)}")
    finally:
        # Clean up temp files
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)
