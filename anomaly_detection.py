import pandas as pd
from typing import List, Optional


def detect_anomalies(data: pd.DataFrame,
                     column: str,
                     lower_threshold: float,
                     upper_threshold: float,
                     group_columns: Optional[List[str]] = None,
                     selected_categories: Optional[dict] = None) -> pd.DataFrame:
    """
    Обнаруживает аномалии в данных на основе заданных порогов.

    Args:
        data: DataFrame с данными для анализа
        column: Название столбца для анализа
        lower_threshold: Нижний порог для обнаружения аномалий
        upper_threshold: Верхний порог для обнаружения аномалий
        group_columns: Список столбцов для группировки (опционально)
        selected_categories: Словарь с выбранными категориями для фильтрации (опционально)

    Returns:
        DataFrame с обнаруженными аномалиями
    """
    if data.empty:
        return pd.DataFrame()

    if group_columns:
        if selected_categories:
            for col, values in selected_categories.items():
                data = data[data[col].isin(values)]
        grouped = data.groupby(group_columns)
        anomalies = pd.DataFrame()
        for name, group in grouped:
            group_anomalies = group[(group[column] < lower_threshold) |
                                    (group[column] > upper_threshold)]
            anomalies = pd.concat([anomalies, group_anomalies])
        return anomalies
    else:
        return data[(data[column] < lower_threshold) |
                    (data[column] > upper_threshold)]


def calculate_stats(data: pd.DataFrame, column: str) -> tuple:
    """
    Рассчитывает статистические показатели для обнаружения аномалий.

    Args:
        data: DataFrame с данными
        column: Название столбца для анализа

    Returns:
        Кортеж (IQR, Q1, Q3)
    """
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    return iqr, q1, q3