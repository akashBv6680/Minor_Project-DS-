import streamlit as st
import pandas as pd
import sweetviz as sv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression  # Example ML model
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="ML Prediction Analysis with Sweetviz",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Analyze ML Predictions with Sweetviz")
st.markdown(
    "Upload a dataset to train a simple Linear Regression model and then analyze its predictions using Sweetviz.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose your data file (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)

        if df is not None and not df.empty:
            st.write("### Original Data Preview:")
            st.dataframe(df.head())
            st.markdown("---")

            st.header("Step 1: Prepare Data for ML")

            # Identify numerical columns for features and target
            numerical_cols = df.select_dtypes(include=np.number).columns.tolist()

            if len(numerical_cols) < 2:
                st.warning("Need at least two numerical columns (features + target) for this example ML model.")
                st.stop()

            feature_cols = st.multiselect(
                "Select Feature Columns (X):",
                numerical_cols,
                default=numerical_cols[:-1] if len(numerical_cols) > 1 else []
            )
            target_col = st.selectbox(
                "Select Target Column (y):",
                [col for col in numerical_cols if col not in feature_cols]
            )

            if not feature_cols or not target_col:
                st.info("Please select at least one feature column and a target column to proceed with ML.")
                st.stop()

            # Prepare X and y
            X = df[feature_cols].dropna()
            y = df.loc[X.index, target_col].dropna()  # Ensure y aligns with X's non-null rows

            if X.empty or y.empty or len(X) != len(y):
                st.error(
                    "Selected columns resulted in empty or mismatched data after dropping NaNs. Please choose different columns or clean your data.")
                st.stop()

            st.write(f"Using {len(feature_cols)} features and '{target_col}' as target.")
            st.markdown("---")

            st.header("Step 2: Train & Predict with a Linear Regression Model")

            if st.button("Train Model and Generate Predictions"):
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                st.info(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

                # Train model
                model = LinearRegression()
                with st.spinner("Training Linear Regression model..."):
                    model.fit(X_train, y_train)
                st.success("Model training complete!")

                # Make predictions
                with st.spinner("Generating predictions..."):
                    y_pred = model.predict(X_test)
                st.success("Predictions generated!")

                # Evaluate model
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                st.write(f"**Model Performance on Test Set:**")
                st.write(f"Mean Squared Error (MSE): `{mse:.2f}`")
                st.write(f"R-squared (R²): `{r2:.2f}`")
                st.markdown("---")

                st.header("Step 3: Analyze Predictions with Sweetviz")
                st.markdown("""
                Now, let's combine the original test features, actual target values, and our model's predictions
                into a new DataFrame and analyze it using Sweetviz!
                """)

                # Create a DataFrame for Sweetviz analysis
                analysis_df = X_test.copy()
                analysis_df['Actual_Target'] = y_test
                analysis_df['Predicted_Target'] = y_pred
                analysis_df['Prediction_Error'] = y_test - y_pred  # Add residuals for analysis

                st.write("### Data for Sweetviz (Test Set + Predictions):")
                st.dataframe(analysis_df.head())

                try:
                    # Generate the Sweetviz report on the augmented DataFrame
                    my_report = sv.analyze(analysis_df,
                                           target_feat='Actual_Target')  # You can set target_feat if desired
                    report_html_path = "sweetviz_predictions_report.html"
                    my_report.save_html(report_html_path)

                    st.success("Sweetviz report on predictions generated!")
                    st.markdown("### Interactive Prediction Analysis Report:")

                    import os

                    if os.path.exists(report_html_path):
                        with open(report_html_path, "rb") as f:
                            html_content = f.read()

                        st.download_button(
                            label="Download Prediction Analysis Report (HTML)",
                            data=html_content,
                            file_name="sweetviz_predictions_report.html",
                            mime="text/html"
                        )
                        st.info("""
                        Click the button above to download the report. In it, you can explore:
                        * The distribution of `Predicted_Target` and `Actual_Target`.
                        * The correlation between `Actual_Target` and `Predicted_Target` (should be high!).
                        * The distribution of `Prediction_Error` (ideally centered around zero).
                        * How individual features relate to both actuals and predictions.
                        """)
                    else:
                        st.error(f"Sweetviz report HTML file not found at {report_html_path}.")

                except Exception as e:
                    st.error(f"Error generating Sweetviz report on predictions: {e}.")
                    st.exception(e)
                finally:
                    if os.path.exists(report_html_path):
                        os.remove(report_html_path)

            else:
                st.info(
                    "Click the button above to start the ML process and generate the Sweetviz report on predictions.")

        else:
            st.warning(
                "The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")

    except Exception as e:
        st.error(f"An error occurred while reading or processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
else:
    st.info("Upload your data file to begin analyzing ML predictions with Sweetviz.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Sweetviz, and Scikit-learn.")