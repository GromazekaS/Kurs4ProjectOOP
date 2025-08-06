import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.vacancy import Vacancy


class Storage(ABC):
    """Абстрактный класс для работы с хранилищем"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONSaver(Storage):
    """Класс для сохранения вакансий в JSON-файл"""

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        self.filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        data = self._read_file()
        vacancy_dict = {
            "title": vacancy.title,
            "link": vacancy.link,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "employer": vacancy.employer,
        }
        data.append(vacancy_dict)
        self._write_file(data)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        data = self._read_file()
        if not criteria:
            return data

        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key == "salary":
                    # Фильтр по зарплате
                    salary = item.get("salary", {})
                    if value == "with_salary" and (salary.get("from") is None and salary.get("to") is None):
                        match = False
                else:
                    # Фильтр по другим полям
                    if value.lower() not in str(item.get(key, "")).lower():
                        match = False
            if match:
                result.append(item)
        return result

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        data = self._read_file()
        new_data = [item for item in data if item["link"] != vacancy.link]
        self._write_file(new_data)

    def _read_file(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
