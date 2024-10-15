import pandas as pd
from typing import List, Optional

def detect_anomalies(data: pd.DataFrame, 
                     column: str, 
                     lower_threshold: float, 
                     upper_threshold: float, 
                     group_columns: Optional[List[str]] = None,
                     selected_categories: Optional[dict] = None) -> pd.DataFrame:
    if group_columns:
        if selected_categories:
            for col, values in selected_categories.items():
                data = data[data[col].isin(values)]
        grouped = data.groupby(group_columns)
        anomalies = pd.DataFrame()
        for name, group in grouped:
            group_anomalies = group[(group[column] < lower_threshold) | (group[column] > upper_threshold)]
            anomalies = pd.concat([anomalies, group_anomalies])
        return anomalies
    else:
        return data[(data[column] < lower_threshold) | (data[column] > upper_threshold)]

def calculate_stats(data: pd.DataFrame, column: str):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    return iqr, q1, q3
