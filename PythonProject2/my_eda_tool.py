import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Suppress warnings that might clutter the Streamlit output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Klib EDA App",
    page_icon="📊",
    layout="wide",  # Use wide layout for better display
    initial_sidebar_state="expanded"
)

st.title("📊 Klib Automated EDA App")
st.markdown("Upload a **CSV** or **Excel (.xlsx)** file to generate Klib visualizations.")

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
            st.write("### Generating Klib Visualizations...")
            st.info("Please wait while Klib analyzes your data and generates plots.")

            try:
                import klib

                with st.spinner("Generating missing value plot..."):
                    st.subheader("1. Missing Value Plot")
                    fig_missing = klib.missingval_plot(df)
                    st.pyplot(fig_missing)  # Display matplotlib figure directly
                    plt.close(fig_missing)  # Close the figure to free up memory

                with st.spinner("Generating correlation plot..."):
                    st.subheader("2. Correlation Plot (Heatmap)")
                    fig_corr = klib.corr_plot(df)
                    st.pyplot(fig_corr)  # Display matplotlib figure directly
                    plt.close(fig_corr)  # Close the figure to free up memory

                st.success("Klib plots generated!")
                st.info(
                    "Klib also provides functions for data cleaning and manipulation. Check its documentation for more features.")

            except Exception as e:
                st.error(f"Error generating Klib plots: {e}.")
                st.exception(e)  # Show full traceback for debugging

        else:
            st.warning(
                "The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
else:
    st.info("Please upload a data file to generate Klib EDA plots.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Klib.")