import streamlit as st
import pandas as pd
import sweetviz as sv
import os
import matplotlib.pyplot as plt
import warnings

# Suppress specific warnings that might clutter the Streamlit output
# These warnings often appear from underlying libraries like numpy, pandas, or matplotlib
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Comprehensive EDA App",
    page_icon="🔎",
    layout="wide",  # Use wide layout for better display of reports
    initial_sidebar_state="expanded"
)

st.title("🔎 Comprehensive Exploratory Data Analysis App")
st.markdown("Upload a **CSV** or **Excel (.xlsx)** file to perform EDA using various Python libraries.")

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

        if df is not None and not df.empty:
            st.write("### Original DataFrame (First 5 rows):")
            st.dataframe(df.head())
            st.markdown("---")
        else:
            st.warning(
                "The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")
            df = None  # Reset df to None if empty or issue

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
        df = None  # Reset df to None on error
else:
    st.info("Please upload a CSV or Excel file to get started with EDA.")

# --- EDA Tool Selection (Conditional Logic) ---
if df is not None:
    eda_tools = [
        "Select an EDA Tool",  # Default/placeholder option
        "Sweetviz",
        "ydata-profiling",  # Formerly pandas-profiling
        "AutoViz",
        "Klib",
        "D-Tale",
        "Dataprep",
        "Pandas-Summary",
        "SpeedML"
    ]

    selected_eda_tool = st.selectbox("Choose an EDA Tool to generate a report/insights:", eda_tools)

    if selected_eda_tool == "Sweetviz":
        st.header("Generating Sweetviz Report...")
        with st.spinner("Generating Sweetviz report... This might take a moment."):
            try:
                sweet_report = sv.analyze(df)
                report_html_path = "sweetviz_report.html"
                sweet_report.save_html(report_html_path)  # Use save_html

                st.success("Sweetviz report generated!")
                st.markdown("### Interactive Report:")

                with open(report_html_path, "rb") as f:
                    html_content = f.read()

                st.download_button(
                    label="Download Sweetviz Report (HTML)",
                    data=html_content,
                    file_name="sweetviz_report.html",
                    mime="text/html"
                )
                st.info(
                    "The interactive Sweetviz report has been generated. Click the button above to download and view it in your browser.")

            except Exception as e:
                st.error(
                    f"Error displaying Sweetviz report: {e}. Please ensure sweetviz and its dependencies are correctly installed and compatible.")
                st.exception(e)  # Show full traceback
            finally:
                if os.path.exists(report_html_path):
                    os.remove(report_html_path)

    elif selected_eda_tool == "ydata-profiling":
        st.header("Generating ydata-profiling Report...")
        try:
            from ydata_profiling import ProfileReport

            with st.spinner("Generating ydata-profiling report... This might take a while for large datasets."):
                profile = ProfileReport(df, title="yData Profiling Report", explorative=True)
                report_html_path = "ydata_profiling_report.html"
                profile.to_file(report_html_path)

                st.success("yData Profiling report generated!")
                st.markdown("### Interactive Report:")

                with open(report_html_path, "rb") as f:
                    html_content = f.read()

                st.download_button(
                    label="Download yData Profiling Report (HTML)",
                    data=html_content,
                    file_name="ydata_profiling_report.html",
                    mime="text/html"
                )
                st.info(
                    "The interactive yData Profiling report has been generated. Click the button above to download and view it in your browser.")

        except Exception as e:
            st.error(f"Error displaying ydata-profiling report: {e}. Ensure the library is installed.")
            st.exception(e)
        finally:
            if os.path.exists(report_html_path):
                os.remove(report_html_path)

    elif selected_eda_tool == "AutoViz":
        st.header("Generating AutoViz Report...")
        try:
            from autoviz.AutoViz_Class import AutoViz_Class

            AV = AutoViz_Class()

            # AutoViz typically takes a filename, so we save DataFrame to a temporary CSV
            temp_csv_path = "temp_autoviz_data.csv"
            df.to_csv(temp_csv_path, index=False)

            report_html_path = "autoviz_report.html"

            with st.spinner("Generating AutoViz report... This can take some time."):
                # AutoViz saves the HTML report to the current directory by default
                # The returned value is often None or a DataFrame.
                dft = AV.AutoViz(
                    filename=temp_csv_path,
                    sep=",",
                    depVar="",  # No dependent variable for general EDA
                    dfte=None,
                    header=0,
                    verbose=0,
                    lowess=False,
                    chart_format="html",  # Ensure HTML output
                    max_rows_analyzed=150000,
                    max_cols_analyzed=30
                )

            st.success("AutoViz report generated!")
            st.markdown("### Interactive Report:")

            with open(report_html_path, "rb") as f:
                html_content = f.read()

            st.download_button(
                label="Download AutoViz Report (HTML)",
                data=html_content,
                file_name="autoviz_report.html",
                mime="text/html"
            )
            st.info(
                "The interactive AutoViz report has been generated. Click the button above to download and view it in your browser.")

        except Exception as e:
            st.error(f"Error generating AutoViz report: {e}. Ensure the library is installed and check data format.")
            st.exception(e)
        finally:
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
            if os.path.exists(report_html_path):
                os.remove(report_html_path)

    elif selected_eda_tool == "Klib":
        st.header("Generating Klib visualizations...")
        try:
            import klib

            with st.spinner("Generating Klib plots..."):
                st.subheader("Missing Value Plot")
                fig_missing = klib.missingval_plot(df)
                st.pyplot(fig_missing)  # Display matplotlib figure

                st.subheader("Correlation Plot (Heatmap)")
                fig_corr = klib.corr_plot(df)
                st.pyplot(fig_corr)  # Display matplotlib figure

                st.success("Klib plots generated!")
                st.info(
                    "Klib also provides functions for data cleaning and manipulation. Check its documentation for more.")

        except Exception as e:
            st.error(f"Error generating Klib plots: {e}. Ensure the library is installed.")
            st.exception(e)

    elif selected_eda_tool == "D-Tale":
        st.header("Launching D-Tale (New Tab)...")
        try:
            import dtale

            # D-Tale runs its own Flask web server. It's usually best to launch it
            # and provide a link to the user.
            d = dtale.show(df, open_browser=False)  # open_browser=False prevents new tab on server
            dtale_url = d._url
            st.success("D-Tale launched!")
            st.markdown(f"D-Tale is running at: [Click here to open D-Tale in a new tab]({dtale_url})")
            st.warning(
                "D-Tale will run in your browser and might open on a different port. Keep this Streamlit app open while using D-Tale. To stop D-Tale, close the tab and refresh this Streamlit app.")
        except Exception as e:
            st.error(
                f"Error launching D-Tale: {e}. Make sure you have `dtale` installed and that the necessary ports are free.")
            st.exception(e)

    elif selected_eda_tool == "Dataprep":
        st.header("Generating Dataprep Report...")
        try:
            from dataprep.eda import create_report

            with st.spinner("Generating Dataprep report... This can be memory intensive."):
                report = create_report(df)
                report_html_path = "dataprep_report.html"
                report.save(report_html_path)  # Save to HTML file

                st.success("Dataprep report generated!")
                st.markdown("### Interactive Report:")

                with open(report_html_path, "rb") as f:
                    html_content = f.read()

                st.download_button(
                    label="Download Dataprep Report (HTML)",
                    data=html_content,
                    file_name="dataprep_report.html",
                    mime="text/html"
                )
                st.info(
                    "The interactive Dataprep report has been generated. Click the button above to download and view it in your browser.")
        except Exception as e:
            st.error(
                f"Error displaying Dataprep report: {e}. Ensure the library is installed and check memory usage for large datasets.")
            st.exception(e)
        finally:
            if os.path.exists(report_html_path):
                os.remove(report_html_path)

    elif selected_eda_tool == "Pandas-Summary":
        st.header("Generating Pandas-Summary Report...")
        try:
            from pandas_summary import DataFrameSummary

            with st.spinner("Generating Pandas-Summary report..."):
                dfs = DataFrameSummary(df)
                st.success("Pandas-Summary generated!")
                st.subheader("DataFrame Summary Statistics:")
                # DataFrameSummary outputs its statistics as a pandas DataFrame
                st.dataframe(dfs.columns_stats)
                st.info("Pandas-Summary provides concise statistics for each column.")
        except Exception as e:
            st.error(f"Error generating Pandas-Summary report: {e}. Ensure the library is installed.")
            st.exception(e)

    elif selected_eda_tool == "SpeedML":
        st.header("Generating SpeedML EDA...")
        try:
            from speedml import SpeedML

            # SpeedML is more geared towards ML pipelines and requires a target column
            # You'll need to know your target column name or select it.
            # For general EDA without a target, its direct use can be limited.

            # --- IMPORTANT: Replace 'your_target_column_name_here' with an actual column from your data ---
            # If you don't have a specific target, you might not use all SpeedML features or need to adapt.
            target_column = st.text_input("Enter target column name for SpeedML (optional):", "")

            if target_column and target_column in df.columns:
                sml = SpeedML(df, target=target_column)
                st.success(f"SpeedML initialized with target: '{target_column}'")

                st.subheader("SpeedML Data Overview (prints to console)")
                # Many SpeedML functions print directly to console, making direct Streamlit display hard.
                st.code("""
# Example SpeedML commands you might run in a script or console:
# sml.eda_all()
# sml.plot_corr()
# sml.plot_dist()
# sml.cont_feats
# sml.nominal_feats
# sml.ordinal_feats
""")
                st.info(
                    "SpeedML's primary output is often to the console or directly manipulate the DataFrame. For full interactive reports, consider other tools like Sweetviz or ydata-profiling.")

                st.subheader("Sample of DataFrame after SpeedML initialization (first 5 rows):")
                st.dataframe(sml.data.head())  # SpeedML stores data in sml.data

            else:
                st.warning(
                    "SpeedML often requires a target column for its most powerful EDA. Please enter a valid target column name from your dataset, or choose another tool for general EDA.")
                st.dataframe(df.head())  # Show original df if no target

        except Exception as e:
            st.error(
                f"Error generating SpeedML EDA: {e}. Ensure the library is installed and a valid target column is provided if needed.")
            st.exception(e)

    elif selected_eda_tool == "Select an EDA Tool":
        st.info("Select an EDA tool from the dropdown above to generate a report after uploading your data.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and various powerful EDA libraries.")