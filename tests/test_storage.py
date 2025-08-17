import pytest
import json
import os
from src.storage import JSONSaver
from src.vacancy import Vacancy

@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "test_vacancies.json"

@pytest.fixture
def sample_vacancy():
    return Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        employer="TechCorp"
    )

def test_add_vacancy(temp_file, sample_vacancy):
    saver = JSONSaver(filename=temp_file)
    saver.add_vacancy(sample_vacancy)
    
    # Проверяем что файл создан
    assert os.path.exists(temp_file)
    
    # Читаем содержимое файла
    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]['title'] == "Python Developer"
        assert data[0]['salary']['from'] == 100000

def test_delete_vacancy(temp_file, sample_vacancy):
    saver = JSONSaver(filename=temp_file)
    
    # Добавляем две вакансии
    saver.add_vacancy(sample_vacancy)
    another_vacancy = Vacancy(
        title="Data Scientist",
        link="https://hh.ru/vacancy/456",
        salary=None,
        description="Machine learning",
        employer="DataCorp"
    )
    saver.add_vacancy(another_vacancy)
    
    # Удаляем одну
    saver.delete_vacancy(sample_vacancy)
    
    # Проверяем содержимое
    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]['title'] == "Data Scientist"

def test_get_vacancies(temp_file, sample_vacancy):
    saver = JSONSaver(filename=temp_file)
    saver.add_vacancy(sample_vacancy)
    
    # Получаем все вакансии
    all_vacancies = saver.get_vacancies()
    assert len(all_vacancies) == 1
    
    # Фильтруем по названию
    filtered = saver.get_vacancies({"title": "Python"})
    assert len(filtered) == 1
    
    # Фильтр, который не должен ничего найти
    not_found = saver.get_vacancies({"title": "Java"})
    assert len(not_found) == 0
    
    # Фильтр по зарплате
    with_salary = saver.get_vacancies({"salary": "with_salary"})
    assert len(with_salary) == 1

def test_empty_file(temp_file):
    saver = JSONSaver(filename=temp_file)
    vacancies = saver.get_vacancies()
    assert vacancies == []

def test_delete_from_empty_file(temp_file, sample_vacancy):
    saver = JSONSaver(filename=temp_file)
    # Не должно быть ошибки при удалении из пустого файла
    saver.delete_vacancy(sample_vacancy)