import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from anomaly_detection import detect_anomalies, calculate_stats
from ui_elements import set_page_config, set_title, set_instructions, set_documentation
from anomaly_processor import process_file, create_anomalies_excel

set_page_config()
set_title()

# Добавляем стили CSS для изменения оформления
st.markdown("""
<style>
.stButton button {
    background-color: #87CEFA; /* Заменено на светло-голубой */
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
}
.stDataFrame {
    background-color: white;
    border-radius: 5px;
    padding: 10px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}
.stSelectbox div[data-baseweb="select"] {
    background-color: #87CEFA !important; /* Заменено на светло-голубой */
    color: white !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #87CEFA !important;
    color: white !important;
}
.stSelectbox div[data-baseweb="select"] > div > div {
    background-color: #87CEFA !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Загрузите файл Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Прочитать загруженный файл как байтовый поток
    file_bytes = uploaded_file.read()
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(BytesIO(file_bytes), engine='openpyxl')
    else:
        df = pd.read_excel(BytesIO(file_bytes), engine='xlrd')
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

    # Новая кнопка для обработки файла и нахождения аномалий по каждому столбцу
    if st.button("Обработать файл и найти аномалии по каждому столбцу"):
        # Сохранение загруженного файла
        with open("uploaded_file.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Обработка файла и отображение результатов
        results = process_file("uploaded_file.xlsx")
        st.write("Результаты обработки:")
        
        # Создаем DataFrame для отображения всех аномалий
        all_anomalies = pd.DataFrame()
        
        for result in results:
            column = result['column']
            anomalies = result['anomalies']
            st.write(f"Столбец: {column}")
            st.dataframe(anomalies)
            
            # Добавляем аномалии в общий DataFrame
            if all_anomalies.empty:
                all_anomalies = anomalies
            else:
                all_anomalies = pd.merge(all_anomalies, anomalies, how='outer')
        
        # Отображаем общую таблицу аномалий
        st.write("Общая таблица аномалий:")
        st.dataframe(all_anomalies)
        
        # Кнопка для скачивания всех аномалий
        if st.button("Скачать все аномалии"):
            excel_data = create_anomalies_excel(results)
            st.download_button(
                label="Скачать все аномалии в Excel",
                data=excel_data,
                file_name="all_anomalies.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

set_instructions()
set_documentation()
