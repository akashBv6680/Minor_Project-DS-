import os
import pandas as pd
import streamlit as st
import sweetviz as sv

st.set_page_config(page_title="Sweetviz EDA App", layout="wide")

st.title("Sweetviz EDA App")
st.write("Upload a CSV or Excel file to generate an interactive Sweetviz report.")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or XLSX file.")
            st.stop()

        st.write("### Original DataFrame (First 5 rows):")
        st.dataframe(df.head())

        st.write("---")
        st.write("### Generating Sweetviz Report...")

        sweetviz_report = sv.analyze(df)
        report_html_path = "sweetviz_report.html"
        sweetviz_report.show_html(filepath=report_html_path, open_browser=False)

        st.success("Sweetviz report generated successfully!")

        with open(report_html_path, "rb") as f:
            st.download_button(
                label="Download Sweetviz Report (HTML)",
                data=f.read(),
                file_name="sweetviz_report.html",
                mime="text/html"
            )

        st.info("The interactive Sweetviz report has been generated. Click the button above to download and view it in your browser.")

        if os.path.exists(report_html_path):
            os.remove(report_html_path)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV or Excel file to get started.")
