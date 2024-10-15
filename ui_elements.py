import streamlit as st

def set_page_config():
    st.set_page_config(page_title="Обнаружение аномалий", layout="wide")

def set_title():
    st.title("Обнаружение аномалий в данных")

def set_instructions():
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

def set_documentation():
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
