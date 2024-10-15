# Anomalizer

## Описание проекта

**Anomalizer** - это инструмент для анализа временных рядов и выявления аномалий с использованием метода межквартильного размаха (IQR). Проект разработан с использованием библиотеки Streamlit для создания интерактивного веб-приложения, которое позволяет пользователям загружать свои данные, настраивать параметры анализа и визуализировать результаты.

## Функциональные возможности

- **Загрузка данных**: Поддержка загрузки файлов Excel с данными.
- **Выбор столбцов**: Возможность выбора столбца с датой для оси X и числового столбца для анализа.
- **Группировка данных**: Поддержка выбора категориальных признаков для группировки данных.
- **Настройка порогов**: Возможность настройки нижнего и верхнего порогов для обнаружения аномалий.
- **Визуализация**: Построение графиков с использованием Plotly для визуализации аномалий.
- **Скачивание результатов**: Возможность скачивания результатов анализа в формате Excel.

## Установка

Рекомендуется использовать `conda` для управления зависимостями и создания изолированной среды. Следуйте этим шагам для настройки проекта:

1. Установите [Anaconda](https://www.anaconda.com/products/distribution) или [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/anomalizer.git
    ```

3. Перейдите в директорию проекта:
    ```sh
    cd anomalizer
    ```

4. Создайте и активируйте новую среду conda:
    ```sh
    conda create --name anomalizer python=3.8
    conda activate anomalizer
    ```

5. Установите зависимости из файла `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

## Использование

1. Запустите приложение Streamlit:
    ```sh
    streamlit run app5.py
    ```
2. Откройте браузер и перейдите по адресу `http://localhost:8501`.
3. Следуйте инструкциям на экране для загрузки данных и настройки параметров анализа.

## Пример использования

1. Загрузите файл Excel с вашими данными.
2. Выберите столбец с датой для оси X (если доступно).
3. Выберите числовой столбец для анализа.
4. Выберите категориальные признаки для группировки (необязательно).
5. Выберите конкретные значения категориальных признаков (если применимо).
6. Настройте нижний и верхний пороги для обнаружения аномалий.
7. Нажмите кнопку "Обнаружить аномалии".
8. Просмотрите результаты и визуализацию.
9. При необходимости скачайте результаты в Excel.

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

## Лицензия

Этот проект лицензирован под лицензией GNU General Public License v3.0. Подробности см. в файле [LICENSE](LICENSE).
