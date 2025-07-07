import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sweetviz as sv
import os

def generate_sweetviz_report(df, report_name="SWEETVIZ_REPORT"):
    # Create a Sweetviz report
    my_report = sv.analyze(df)

    # Define the path to save the HTML report
    report_html_path = f"{report_name}.html"

    # Save the report as HTML without opening in browser
    # Ensure your sweetviz version supports save_html or show_html with filepath
    my_report.save_html(report_html_path)
    # Alternatively: my_report.show_html(report_html_path, open_browser=False)

    return report_html_path

st.title("Sweetviz EDA in Streamlit")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Data Head:")
        st.dataframe(df.head())

        st.subheader("Generating Sweetviz Report...")
        report_path = generate_sweetviz_report(df)

        # Read the generated HTML file
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Embed the HTML content in Streamlit using components.html
        # Adjust width and height as needed
        components.html(html_content, height=1000, scrolling=True)

        # Clean up the generated HTML file (optional)
        os.remove(report_path)

    except Exception as e:
        st.error(f"An error occurred while reading or processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")