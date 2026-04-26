import pandas as pd
import numpy as np
from scipy import stats
from pandas.api.types import is_numeric_dtype

def analyze_data(df):
    report = {}
    total_cells = df.size
    total_rows = len(df)
    missing = df.isnull().sum().sum()
    report["missing_values_count"] = missing
    report["missing_values_percent"] = (missing / total_cells) * 100 if total_cells > 0 else 0
    duplicates = df.duplicated().sum()
    report["duplicates"] = duplicates
    report["duplicates_percent"] = (duplicates / total_rows) * 100 if total_rows > 0 else 0

    # outliers
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_values = df[numeric_cols].size if len(numeric_cols) > 0 else 0
    outliers = 0
    for col in numeric_cols:
        nonna = df[col].dropna()
        if nonna.shape[0] > 1:
            z = np.abs(stats.zscore(nonna))
            outliers += (z >= 3).sum()
    report["outliers"] = outliers
    report["outliers_percent"] = (outliers / numeric_values) * 100 if numeric_values > 0 else 0

    return report

def score_data(df, report):
    missing_penalty = report["missing_values_percent"] * 2.0
    duplicate_penalty = report["duplicates_percent"] * 4.0
    outlier_penalty = report["outliers_percent"] * 3.0

    score = 100 - missing_penalty - duplicate_penalty - outlier_penalty
    return max(0, min(100, int(score)))

def clean_data(df):
    df = df.copy()

    # fill missing values
    for col in df.columns:
        if is_numeric_dtype(df[col].dtype):
            mean_val = df[col].mean()
            if not np.isnan(mean_val):
                df[col] = df[col].fillna(mean_val)
            else:
                median_val = df[col].median()
                if not np.isnan(median_val):
                    df[col] = df[col].fillna(median_val)
                else:
                    df[col] = df[col].fillna(0)
        else:
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
            else:
                df[col] = df[col].fillna("Unknown")

    # remove duplicates
    df = df.drop_duplicates()

    # remove outliers
    df = remove_outliers(df)

    return df

def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        nonna = df[col].dropna()
        if nonna.shape[0] > 1:  # need at least 2 values for zscore
            z = np.abs(stats.zscore(nonna))
            mask = pd.Series(True, index=df.index)
            mask.loc[nonna.index] = z < 3
            df = df.loc[mask]
    return df