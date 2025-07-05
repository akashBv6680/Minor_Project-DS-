import streamlit as st
import pandas as pd
import warnings

# Suppress warnings that might clutter the Streamlit output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="D-Tale EDA App",
    page_icon="📊",
    layout="wide", # Use wide layout for better display
    initial_sidebar_state="expanded"
)

st.title("📊 D-Tale Interactive EDA App")
st.markdown("Upload a **CSV** or **Excel (.xlsx)** file to launch an interactive D-Tale session.")

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
            st.stop() # Stop execution if file type is not supported

        if df is not None and not df.empty:
            st.write("### Original DataFrame (First 5 rows):")
            st.dataframe(df.head())

            st.markdown("---")
            st.write("### Launching D-Tale Interactive Session...")
            st.info("D-Tale will open in a new browser tab. Please keep this Streamlit app open while using D-Tale.")

            try:
                import dtale
                # open_browser=False prevents D-Tale from trying to open a new tab on the server itself.
                # It returns a D-Tale instance from which we can get the URL.
                d = dtale.show(df, open_browser=False)
                dtale_url = d._url

                st.success("D-Tale session started!")
                st.markdown(f"Click here to open D-Tale in a new tab: [**{dtale_url}**]({dtale_url})")
                st.warning("To stop the D-Tale session, simply close the D-Tale browser tab and then refresh this Streamlit app.")

            except Exception as e:
                st.error(f"Error launching D-Tale: {e}.")
                st.exception(e) # Show full traceback for debugging

        else:
            st.warning("The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
else:
    st.info("Please upload a data file to launch the D-Tale interactive session.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and D-Tale.")