from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def get_vacancies(self, search_query: str, area_id: int = 113, per_page: int = 100) -> List[Dict[str, Any]]:
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "VacancyParser/1.0 (support@example.ru)"}

    def get_vacancies(self, search_query: str, area_id: int = 113, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получение вакансий по запросу"""
        params = {
            "text": search_query,
            "area": area_id,  # 113 - Россия
            "per_page": per_page,
            "page": 0,
            "only_with_salary": True,
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()["items"]
        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []
