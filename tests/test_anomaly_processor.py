import pandas as pd
import pytest
import tempfile
import os
from anomaly_processor import process_file, display_results, create_anomalies_excel


@pytest.fixture
def test_excel_file():
    """Создает временный Excel файл для тестирования."""
    data = {
        'date': pd.date_range('2023-01-01', periods=10),
        'temperature': [20, 22, 21, 50, 19, 18, 20, 21, 100, 22],  # 50 и 100 - аномалии
        'humidity': [60, 62, 61, 59, 58, 200, 61, 60, 59, 62],  # 200 - аномалия
        'category': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A']
    }
    df = pd.DataFrame(data)
    
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
    
    # Удаляем файл после использования
    os.unlink(tmp.name)


@pytest.fixture
def test_results():
    """Создает тестовые результаты для проверки функций."""
    return [
        {
            'column': 'temperature',
            'anomalies': pd.DataFrame({
                'temperature': [50, 100],
                'date': pd.to_datetime(['2023-01-04', '2023-01-09'])
            }),
            'lower_threshold': 15,
            'upper_threshold': 25
        },
        {
            'column': 'humidity',
            'anomalies': pd.DataFrame({
                'humidity': [200],
                'date': pd.to_datetime(['2023-01-06'])
            }),
            'lower_threshold': 55,
            'upper_threshold': 65
        }
    ]


class TestProcessFile:
    """Тесты для функции process_file."""
    
    def test_process_file_basic(self, test_excel_file):
        """Проверяет базовую обработку файла."""
        results = process_file(test_excel_file)
        
        # Проверяем, что обработаны только числовые столбцы
        column_names = [r['column'] for r in results]
        assert 'temperature' in column_names
        assert 'humidity' in column_names
        assert 'category' not in column_names
        assert 'date' not in column_names
    
    def test_process_file_finds_anomalies(self, test_excel_file):
        """Проверяет, что функция находит аномалии."""
        results = process_file(test_excel_file)
        
        # Проверяем аномалии в температуре
        temp_result = next(r for r in results if r['column'] == 'temperature')
        temp_anomalies = temp_result['anomalies']
        assert len(temp_anomalies) >= 2  # Должны найти как минимум 50 и 100
        assert 50 in temp_anomalies['temperature'].values
        assert 100 in temp_anomalies['temperature'].values
        
        # Проверяем аномалии во влажности
        humidity_result = next(r for r in results if r['column'] == 'humidity')
        humidity_anomalies = humidity_result['anomalies']
        assert len(humidity_anomalies) >= 1  # Должны найти как минимум 200
        assert 200 in humidity_anomalies['humidity'].values
    
    def test_process_file_empty_excel(self):
        """Проверяет обработку пустого файла."""
        # Создаем пустой Excel файл
        df = pd.DataFrame()
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            temp_name = tmp.name
            df.to_excel(temp_name, index=False)
        
        try:
            results = process_file(temp_name)
            assert results == []
        finally:
            os.unlink(temp_name)
    
    def test_process_file_no_numeric_columns(self):
        """Проверяет обработку файла без числовых столбцов."""
        # Создаем файл только с текстовыми столбцами
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'city': ['NYC', 'LA', 'Chicago']
        })
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            temp_name = tmp.name
            df.to_excel(temp_name, index=False)
        
        try:
            results = process_file(temp_name)
            assert results == []
        finally:
            os.unlink(temp_name)


class TestDisplayResults:
    """Тесты для функции display_results."""
    
    def test_display_results_output(self, test_results, capsys):
        """Проверяет вывод результатов в консоль."""
        display_results(test_results)
        
        captured = capsys.readouterr()
        assert "Столбец: temperature" in captured.out
        assert "Столбец: humidity" in captured.out
        assert "50" in captured.out  # Проверяем, что аномалии выводятся
        assert "100" in captured.out
        assert "200" in captured.out
    
    def test_display_results_empty(self, capsys):
        """Проверяет вывод пустых результатов."""
        display_results([])
        
        captured = capsys.readouterr()
        assert captured.out == ""  # Ничего не должно выводиться


class TestCreateAnomaliesExcel:
    """Тесты для функции create_anomalies_excel."""
    
    def test_create_anomalies_excel_basic(self, test_results):
        """Проверяет создание Excel файла с аномалиями."""
        excel_data = create_anomalies_excel(test_results)
        
        # Проверяем, что возвращаются байты
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0
        
        # Проверяем, что файл можно прочитать
        df = pd.read_excel(pd.io.common.BytesIO(excel_data))
        assert 'Anomaly' in df.columns
        assert len(df) == 3  # Всего 3 аномалии в test_results
    
    def test_create_anomalies_excel_empty(self):
        """Проверяет создание Excel для пустых результатов."""
        excel_data = create_anomalies_excel([])
        
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0
        
        # Проверяем, что файл содержит пустой DataFrame
        df = pd.read_excel(pd.io.common.BytesIO(excel_data))
        assert len(df) == 0
    
    def test_create_anomalies_excel_no_anomalies(self):
        """Проверяет создание Excel когда нет аномалий."""
        results = [
            {
                'column': 'test_column',
                'anomalies': pd.DataFrame(),  # Пустой DataFrame
                'lower_threshold': 0,
                'upper_threshold': 100
            }
        ]
        
        excel_data = create_anomalies_excel(results)
        
        assert isinstance(excel_data, bytes)
        df = pd.read_excel(pd.io.common.BytesIO(excel_data))
        assert len(df) == 0