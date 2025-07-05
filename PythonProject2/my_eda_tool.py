import streamlit as st
import pandas as pd
import warnings

# Suppress warnings that might clutter the Streamlit output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Pandas-Summary EDA App",
    page_icon="📋",
    layout="wide",  # Use wide layout for better display
    initial_sidebar_state="expanded"
)

st.title("📋 Pandas-Summary Exploratory Data Analysis App")
st.markdown("Upload a **CSV** or **Excel (.xlsx)** file to generate a Pandas-Summary report.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a data file", type=["csv", "xlsx"])

df = None
if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_type}. Please upload a CSV or XLSX file.")
            st.stop()  # Stop execution if file type is not supported

        if df is not None and not df.empty:
            st.write("### Original DataFrame (First 5 rows):")
            st.dataframe(df.head())

            st.markdown("---")
            st.write("### Generating Pandas-Summary Report...")
            st.info("Please wait while Pandas-Summary analyzes your data.")

            try:
                from pandas_summary import DataFrameSummary

                with st.spinner("Calculating summary statistics..."):
                    # Generate the DataFrameSummary
                    dfs = DataFrameSummary(df)

                st.success("Pandas-Summary report generated!")
                st.write("### DataFrame Summary Statistics:")

                # DataFrameSummary outputs its statistics as a pandas DataFrame
                # We display the 'columns_stats' which gives an overview of each column
                st.dataframe(dfs.columns_stats)

                st.info(
                    "Pandas-Summary provides concise statistics for each column, including missing values, unique counts, and typical descriptive stats.")

            except Exception as e:
                st.error(f"Error generating Pandas-Summary report: {e}.")
                st.exception(e)  # Show full traceback for debugging

        else:
            st.warning(
                "The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
else:
    st.info("Please upload a data file to generate the Pandas-Summary report.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Pandas-Summary.")