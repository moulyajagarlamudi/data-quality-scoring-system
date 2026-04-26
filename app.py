import streamlit as st
import pandas as pd
from data_cleaning import analyze_data, clean_data, score_data

st.title("AI Data Quality Scoring System")

file = st.file_uploader("Upload CSV file")

if file:
    df = pd.read_csv(file)
    st.write("### Original Data")
    st.write(df.head(10))
    st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")

    report = analyze_data(df)
    st.write("### Analysis Report")
    st.write(f"Missing values: {report['missing_values_count']} ({report['missing_values_percent']:.1f}%)")
    st.write(f"Duplicates: {report['duplicates']} ({report['duplicates_percent']:.1f}%)")
    st.write(f"Outliers detected: {report['outliers']} ({report['outliers_percent']:.1f}% of numeric values)")

    initial_score = score_data(df, report)
    st.write(f"Initial Data Quality Score: {initial_score}/100")

    cleaned_df = clean_data(df)
    final_report = analyze_data(cleaned_df)
    final_score = score_data(cleaned_df, final_report)

    rows_removed = len(df) - len(cleaned_df)
    missing_filled = report['missing_values_count'] - final_report['missing_values_count']
    duplicates_removed = report['duplicates'] - final_report['duplicates']
    outliers_removed = report['outliers'] - final_report['outliers']

    st.write("### Cleaned Data Summary")
    st.write(f"Rows removed: {rows_removed}")
    st.write(f"Missing values filled: {missing_filled}")
    st.write(f"Duplicates removed: {duplicates_removed}")
    st.write(f"Outliers removed: {outliers_removed}")
    st.write(f"Final Data Quality Score: {final_score}/100")

    st.write("### Cleaned Data")
    st.write(cleaned_df.head(10))

    st.download_button("Download Cleaned Data",
                       cleaned_df.to_csv(index=False),
                       "cleaned_data.csv",
                       mime="text/csv")