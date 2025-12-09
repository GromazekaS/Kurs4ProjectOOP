import requests
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod


class JobAPI(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_employer_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self) -> None:
        self.__base_url: str = "https://api.hh.ru"
        self.__headers: Dict[str, str] = {"User-Agent": "VacancyParser/1.0"}

    def connect(self) -> None:
        """Публичный метод подключения"""
        self.__connect_api()

    def __connect_api(self) -> None:
        """Приватный метод для реального подключения к API"""
        # Проверка доступности API
        try:
            response = requests.get(f"{self.__base_url}/employers/1", headers=self.__headers)
            response.raise_for_status()
        except requests.RequestException:
            print("Ошибка подключения к API HeadHunter")

    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        """Получение информации о работодателе"""
        self.connect()
        try:
            response = requests.get(
                f"{self.__base_url}/employers/{employer_id}",
                headers=self.__headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении данных работодателя: {e}")
            return {}

    def get_employer_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Получение вакансий работодателя"""
        self.connect()
        params = {
            "employer_id": employer_id,
            "per_page": 100,
            "page": 0,
            "only_with_salary": True
        }
        try:
            response = requests.get(
                f"{self.__base_url}/vacancies",
                params=params,
                headers=self.__headers
            )
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []