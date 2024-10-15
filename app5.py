import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import List, Optional
from io import BytesIO

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

st.set_page_config(page_title="Обнаружение аномалий", layout="wide")
st.title("Обнаружение аномалий в данных")

uploaded_file = st.file_uploader("Загрузите файл Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Предварительный просмотр данных:")
    st.dataframe(df.head())

    date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    if date_columns:
        date_column = st.selectbox("Выберите столбец с датой для оси X", date_columns)
        df[date_column] = pd.to_datetime(df[date_column])
    else:
        st.warning("В датасете не обнаружены столбцы с датами. Будет использован индекс.")
        date_column = None

    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_column = st.selectbox("Выберите числовой столбец для анализа", numeric_columns)

    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    group_columns = st.multiselect("Выберите категориальные признаки для группировки (необязательно)", categorical_columns)

    selected_categories = {}
    if group_columns:
        for col in group_columns:
            unique_values = df[col].unique()
            selected_values = st.multiselect(f"Выберите значения для {col}", unique_values, default=unique_values)
            selected_categories[col] = selected_values

    if group_columns and selected_categories:
        filtered_df = df[df[group_columns].isin(selected_categories).all(axis=1)]
    else:
        filtered_df = df

    iqr, q1, q3 = calculate_stats(filtered_df, selected_column)

    col1, col2, col3 = st.columns(3)
    with col1:
        lower_threshold = st.number_input("Нижний порог", value=float(q1 - 1.5 * iqr))
    with col2:
        upper_threshold = st.number_input("Верхний порог", value=float(q3 + 1.5 * iqr))
    with col3:
        st.write("IQR (Межквартильный размах):", round(iqr, 4))
        st.write("Q1 (25-й процентиль):", round(q1, 4))
        st.write("Q3 (75-й процентиль):", round(q3, 4))

    if st.button("Обнаружить аномалии"):
        anomalies = detect_anomalies(filtered_df, selected_column, lower_threshold, upper_threshold, group_columns, selected_categories)

        st.write(f"Обнаружено {len(anomalies)} аномалий")

        fig = go.Figure()

        if group_columns:
            for name, group in filtered_df.groupby(group_columns):
                group_anomalies = anomalies[anomalies[group_columns].apply(tuple, axis=1).isin(group[group_columns].apply(tuple, axis=1))]
                x_values = group[date_column] if date_column else group.index
                fig.add_trace(go.Scatter(x=x_values, y=group[selected_column], mode='markers', name=f'Данные: {name}', opacity=0.5))
                fig.add_trace(go.Scatter(x=group_anomalies[date_column] if date_column else group_anomalies.index, 
                                         y=group_anomalies[selected_column], mode='markers', 
                                         name=f'Аномалии: {name}', marker=dict(color='red', size=10)))
        else:
            x_values = filtered_df[date_column] if date_column else filtered_df.index
            fig.add_trace(go.Scatter(x=x_values, y=filtered_df[selected_column], mode='markers', name='Данные', opacity=0.5))
            fig.add_trace(go.Scatter(x=anomalies[date_column] if date_column else anomalies.index, 
                                     y=anomalies[selected_column], mode='markers', 
                                     name='Аномалии', marker=dict(color='red', size=10)))

        fig.add_hline(y=lower_threshold, line_dash="dash", line_color="red", annotation_text="Нижний порог")
        fig.add_hline(y=upper_threshold, line_dash="dash", line_color="red", annotation_text="Верхний порог")

        fig.update_layout(title=f"Обнаружение аномалий в столбце {selected_column}", 
                          xaxis_title="Дата" if date_column else "Индекс", 
                          yaxis_title="Значение",
                          hovermode="closest")

        st.plotly_chart(fig, use_container_width=True)

        st.write("Аномальные значения:")
        st.dataframe(anomalies)

        if not anomalies.empty:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                anomalies.to_excel(writer, index=False, sheet_name='Аномалии')
            excel_data = output.getvalue()
            st.download_button(
                label="Скачать аномалии в Excel",
                data=excel_data,
                file_name="anomalies.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

st.markdown("""
### Инструкции:
1. Загрузите файл Excel с вашими данными.
2. Выберите столбец с датой для оси X (если доступно).
3. Выберите числовой столбец для анализа.
4. Выберите категориальные признаки для группировки (необязательно).
5. Выберите конкретные значения категориальных признаков (если применимо).
6. Настройте нижний и верхний пороги для обнаружения аномалий.
7. Нажмите кнопку "Обнаружить аномалии".
8. Просмотрите результаты и визуализацию.
9. При необходимости скачайте результаты в Excel.
""")

st.markdown("""
## Документация

### Метод межквартильного размаха (IQR) для определения выбросов

Межквартильный размах (IQR) - это статистическая мера разброса данных, которая используется для выявления выбросов в наборе данных. Этот метод устойчив к экстремальным значениям и эффективен для несимметричных распределений.

#### Шаги метода:

1. **Сортировка данных**
   - Упорядочиваем все значения по возрастанию.

2. **Нахождение квартилей**
   - Q1 (первый квартиль): 25-й процентиль
   - Q2 (медиана): 50-й процентиль
   - Q3 (третий квартиль): 75-й процентиль

3. **Расчет межквартильного размаха (IQR)**
   - IQR = Q3 - Q1

4. **Определение границ выбросов**
   - Нижняя граница = Q1 - (множитель * IQR)
   - Верхняя граница = Q3 + (множитель * IQR)
   - Стандартный множитель: 1.5

5. **Выявление выбросов**
   - Любые значения, выходящие за пределы этих границ, считаются выбросами.

#### Влияние множителя IQR

- Увеличение множителя делает метод менее чувствительным (меньше значений определяется как выбросы).
- Уменьшение множителя делает метод более чувствительным (больше значений определяется как выбросы).

Выбор множителя зависит от специфики данных и целей анализа. Стандартное значение 1.5 подходит для многих случаев, но может быть скорректировано в зависимости от требуемой строгости выявления аномалий.

Этот метод эффективен для первичного анализа данных и выявления потенциальных аномалий, но следует учитывать контекст данных при интерпретации результатов.
""")
