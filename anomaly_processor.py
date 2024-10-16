import pandas as pd
import numpy as np
from anomaly_detection import detect_anomalies, calculate_stats
import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill

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
                'anomalies': anomalies,
                'lower_threshold': lower_threshold,
                'upper_threshold': upper_threshold
            })

    return results

def display_results(results):
    for result in results:
        column = result['column']
        anomalies = result['anomalies']
        print(f"Столбец: {column}")
        print(f"Аномалии:\n{anomalies}\n")

def create_anomalies_excel(results):
    all_anomalies = pd.DataFrame()
    
    for result in results:
        column = result['column']
        anomalies = result['anomalies']
        if not anomalies.empty:
            anomalies['Anomaly'] = anomalies[column].astype(str) + ' ' + column
            if all_anomalies.empty:
                all_anomalies = anomalies
            else:
                all_anomalies = pd.concat([all_anomalies, anomalies], axis=0)
    
    all_anomalies = all_anomalies.reset_index(drop=True)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        all_anomalies.to_excel(writer, sheet_name='All Anomalies', index=False)
        workbook = writer.book
        worksheet = workbook['All Anomalies']
        
        red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
            for cell in row:
                if cell.column_letter != 'A' and cell.value is not None:  # Исключаем столбец Date
                    column_name = worksheet.cell(row=1, column=cell.column).value
                    if f"{cell.value} {column_name}" in all_anomalies['Anomaly'].values:
                        cell.fill = red_fill
    
    return output.getvalue()

# Пример использования
if __name__ == "__main__":
    file_path = 'path_to_your_file.xlsx'
    results = process_file(file_path)
    display_results(results)
