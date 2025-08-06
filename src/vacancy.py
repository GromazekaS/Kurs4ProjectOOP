from typing import Dict, List, Any, Optional


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(self, title: str, link: str, salary: Optional[Dict[str, Any]], description: str, employer:str) -> None:
        self.title = title
        self.link = link
        self.salary = self.validate_salary(salary)
        self.description = description
        self.employer = employer

    def validate_salary(self, salary_data: Optional[Dict[str, Any]]) -> dict:
        """Валидация и нормализация данных о зарплате"""
        if not salary_data:
            return {"from": 0, "to": 0, "currency": "не указана"}

        salary_from = salary_data.get("from") or 0
        salary_to = salary_data.get("to") or 0
        currency = salary_data.get("currency", "RUR")

        return {
            "from": salary_from,
            "to": salary_to,
            "currency": currency
        }

    @property
    def avg_salary(self) -> float:
        """Расчет средней зарплаты"""
        if self.salary["from"] and self.salary["to"]:
            return (self.salary["from"] + self.salary["to"]) / 2
        return float(self.salary["from"] or self.salary["to"] or 0)

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по средней зарплате (меньше)"""
        return self.avg_salary < other.avg_salary

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по средней зарплате (больше)"""
        return self.avg_salary > other.avg_salary

    def __str__(self) -> str:
        salary_info = ""
        if self.salary["from"] or self.salary["to"]:
            salary_info = f"{self.salary['from']}-{self.salary['to']} {self.salary['currency']}"
        else:
            salary_info = "Зарплата не указана"

        return (
            f"Вакансия: {self.title}\n"
            f"Компания: {self.employer}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self.description}...\n"
            f"Ссылка: {self.link}\n"
            "----------------------------------"
        )

    @staticmethod
    def cast_to_object_list(vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
        """Преобразование JSON-данных в список объектов Vacancy"""
        vacancies = []
        for item in vacancies_data:
            vacancy = Vacancy(
                title=item.get("name", "Без названия"),
                link=item.get("alternate_url", "#"),
                salary=item.get("salary"),
                description=item.get("snippet", {}).get("requirement", ""),
                employer=item.get("employer", {}).get("name", "Неизвестно")
            )
            vacancies.append(vacancy)
        return vacancies