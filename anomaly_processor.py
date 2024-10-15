import pandas as pd
import numpy as np
from anomaly_detection import detect_anomalies, calculate_stats

def process_file(file_path):
    # Чтение файла
    df = pd.read_excel(file_path)
    
    # Список для хранения результатов
    results = []

    # Проход по каждому столбцу
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # Вычисление статистик
            iqr, q1, q3 = calculate_stats(df, column)
            lower_threshold = q1 - 1.5 * iqr
            upper_threshold = q3 + 1.5 * iqr

            # Нахождение аномалий
            anomalies = detect_anomalies(df, column, lower_threshold, upper_threshold)
            results.append({
                'column': column,
                'anomalies': anomalies
            })

    return results

def display_results(results):
    for result in results:
        column = result['column']
        anomalies = result['anomalies']
        print(f"Столбец: {column}")
        print(f"Аномалии:\n{anomalies}\n")

# Пример использования
if __name__ == "__main__":
    file_path = 'path_to_your_file.xlsx'
    results = process_file(file_path)
    display_results(results)