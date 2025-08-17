import pytest
import requests
from src.external_api import HeadHunterAPI
from unittest.mock import patch, MagicMock

def test_hh_api_initialization():
    api = HeadHunterAPI()
    assert api.base_url == "https://api.hh.ru/vacancies"
    assert "User-Agent" in api.headers

@patch('requests.get')
def test_get_vacancies_success(mock_get):
    # Настраиваем мок-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"id": "1", "name": "Python Developer"},
            {"id": "2", "name": "Data Scientist"}
        ]
    }
    mock_get.return_value = mock_response
    
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")
    
    assert len(vacancies) == 2
    assert vacancies[0]['name'] == "Python Developer"
    assert mock_get.called

@patch('requests.get')
def test_get_vacancies_failure(mock_get):
    # Настраиваем мок для ошибки
    mock_get.side_effect = requests.RequestException("Connection error")
    
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")
    
    assert vacancies == []
    assert mock_get.called

@patch('requests.get')
def test_get_vacancies_with_params(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response
    
    api = HeadHunterAPI()
    api.get_vacancies("Java", area_id=2, per_page=50)
    
    # Проверяем параметры запроса
    mock_get.assert_called_with(
        "https://api.hh.ru/vacancies",
        headers=api.headers,
        params={
            "text": "Java",
            "area": 2,
            "per_page": 50,
            "page": 0,
            "only_with_salary": True
        }
    )