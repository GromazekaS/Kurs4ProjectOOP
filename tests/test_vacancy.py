import pytest
from src.vacancy import Vacancy

def test_vacancy_creation():
    vacancy = Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        employer="TechCorp"
    )
    
    assert vacancy.title == "Python Developer"
    assert vacancy.link == "https://hh.ru/vacancy/123"
    assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUR"}
    assert vacancy.description == "Разработка на Python"
    assert vacancy.employer == "TechCorp"
    assert vacancy.avg_salary == 125000

def test_vacancy_without_salary():
    vacancy = Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary=None,
        description="Разработка на Python",
        employer="TechCorp"
    )
    
    assert vacancy.salary == {"from": 0, "to": 0, "currency": "не указана"}
    assert vacancy.avg_salary == 0

def test_vacancy_comparison():
    vacancy1 = Vacancy("A", "link1", {"from": 100000, "to": 150000}, "desc", "Emp1")
    vacancy2 = Vacancy("B", "link2", {"from": 120000, "to": 180000}, "desc", "Emp2")
    vacancy3 = Vacancy("C", "link3", None, "desc", "Emp3")
    
    # Тестирование операторов сравнения
    assert vacancy2 > vacancy1
    assert vacancy1 < vacancy2
    assert vacancy1 != vacancy2

    # Вакансии без зарплаты должны быть меньше
    assert vacancy3 < vacancy1
    assert vacancy1 > vacancy3

def test_cast_to_object_list():
    vacancies_data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Опыт работы 3 года"},
            "employer": {"name": "Company A"}
        },
        {
            "name": "Data Scientist",
            "alternate_url": "https://hh.ru/vacancy/456",
            "salary": None,
            "snippet": {"requirement": "Machine learning"},
            "employer": {"name": "Company B"}
        }
    ]
    
    vacancies = Vacancy.cast_to_object_list(vacancies_data)
    
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].salary["from"] == 100000
    assert vacancies[1].salary["currency"] == "не указана"

def test_vacancy_str_representation():
    vacancy = Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        employer="TechCorp"
    )
    
    result = str(vacancy)
    assert "Python Developer" in result
    assert "100000-150000 RUR" in result
    assert "TechCorp" in result
    assert "https://hh.ru/vacancy/123" in result