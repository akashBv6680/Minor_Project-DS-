import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# For EDA & plots
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

st.set_page_config(page_title="📊 EDA with Profiling", layout="wide")

st.title("📈 Exploratory Data Analysis (EDA) App")
st.markdown("Upload a dataset (CSV or Excel) and generate an interactive Pandas Profiling report.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📂 Raw Data")
        st.dataframe(df.head())

        st.subheader("🧠 Pandas Profiling Report")
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)

    except Exception as e:
        st.error(f"❌ Error reading the file: {e}")
else:
    st.warning("Please upload a CSV or Excel file to proceed.")
