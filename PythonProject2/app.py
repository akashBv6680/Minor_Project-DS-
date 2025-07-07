import streamlit as st
import pandas as pd
import sweetviz as sv
import os

st.set_page_config(layout="wide")

st.title("Sweetviz EDA App")
st.write("Upload a CSV or Excel file to generate an interactive Sweetviz report.")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Determine file type and read accordingly
    file_extension = uploaded_file.name.split('.')[-1]
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

    # Generate the Sweetviz report
    # Analyze the DataFrame
    sweetviz_report = sv.analyze(df)

    # Save the report to a temporary HTML file
    report_html_path = "sweetviz_report.html"
    sweetviz_report.show_html(filepath=report_html_path, open_browser=False)

    st.success("Sweetviz report generated!")

    # Display the HTML report using Streamlit's components
    # As direct embedding of HTML is limited, we provide a download link
    st.download_button(
        label="Download Sweetviz Report (HTML)",
        data=open(report_html_path, 'rb').read(),
        file_name="sweetviz_report.html",
        mime="text/html"
    )

    st.info(
        f"The interactive Sweetviz report has been generated. Click the button above to download and view it in your browser.")

    # Clean up the temporary HTML file
    if os.path.exists(report_html_path):
        os.remove(report_html_path)

else:
    st.info("Please upload a CSV or Excel file to get started.")