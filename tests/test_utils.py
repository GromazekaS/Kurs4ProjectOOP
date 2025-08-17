import pytest
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies
from src.vacancy import Vacancy

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Developer", "link1", 
                {"from": 100000, "to": 150000, "currency": "RUR"}, 
                "Разработка на Python", "Company A"),
        Vacancy("Java Developer", "link2", 
                {"from": 90000, "to": 120000, "currency": "RUR"}, 
                "Разработка на Java", "Company B"),
        Vacancy("Data Scientist", "link3", 
                {"from": 150000, "to": 200000, "currency": "RUR"}, 
                "Анализ данных, Machine Learning", "Company C"),
        Vacancy("DevOps Engineer", "link4", 
                None, 
                "Настройка инфраструктуры", "Company D")
    ]

def test_filter_vacancies(sample_vacancies):
    # Фильтр без ключевых слов
    result = filter_vacancies(sample_vacancies, [])
    assert len(result) == 4
    
    # Фильтр с одним ключевым словом
    result = filter_vacancies(sample_vacancies, ["Python"])
    assert len(result) == 1
    assert result[0].title == "Python Developer"
    
    # Фильтр с несколькими ключевыми словами
    result = filter_vacancies(sample_vacancies, ["data", "machine"])
    assert len(result) == 1
    assert result[0].title == "Data Scientist"
    
    # Фильтр, который не должен ничего найти
    result = filter_vacancies(sample_vacancies, ["PHP"])
    assert len(result) == 0

def test_sort_vacancies(sample_vacancies):
    sorted_vacancies = sort_vacancies(sample_vacancies)
    
    # Проверяем порядок сортировки (по убыванию зарплаты)
    assert sorted_vacancies[0].title == "Data Scientist"  # avg 175000
    assert sorted_vacancies[1].title == "Python Developer"  # avg 125000
    assert sorted_vacancies[2].title == "Java Developer"  # avg 105000
    assert sorted_vacancies[3].title == "DevOps Engineer"  # нет зарплаты

def test_get_top_vacancies(sample_vacancies):
    # Получаем топ 2
    sorted_vacancies = sort_vacancies(sample_vacancies)
    top = get_top_vacancies(sorted_vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Data Scientist"
    assert top[1].title == "Python Developer"
    
    # Запрашиваем больше, чем есть
    top = get_top_vacancies(sample_vacancies, 10)
    assert len(top) == 4
    
    # Запрашиваем 0
    top = get_top_vacancies(sample_vacancies, 0)
    assert len(top) == 0
    
    # Отрицательное число
    top = get_top_vacancies(sample_vacancies, -5)
    assert len(top) == 0