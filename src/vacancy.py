from typing import Dict, Any, Optional, List


class Vacancy:
    __slots__ = ('__title', '__link', '__salary', '__description', '__employer')

    def __init__(
            self,
            title: str,
            link: str,
            salary: Optional[Dict[str, Any]],
            description: str,
            employer: str
    ) -> None:
        self.__title: str = title
        self.__link: str = link
        self.__salary: Dict[str, Any] = self.__validate_salary(salary)
        self.__description: str = description
        self.__employer: str = employer

    def __validate_salary(self, salary_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
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
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    @property
    def salary(self) -> Dict[str, Any]:
        return self.__salary

    @property
    def description(self) -> str:
        return self.__description

    @property
    def employer(self) -> str:
        return self.__employer

    @property
    def avg_salary(self) -> float:
        if self.__salary["from"] and self.__salary["to"]:
            return (self.__salary["from"] + self.__salary["to"]) / 2
        return self.__salary["from"] or self.__salary["to"] or 0

    def __lt__(self, other: 'Vacancy') -> bool:
        return self.avg_salary < other.avg_salary

    def __gt__(self, other: 'Vacancy') -> bool:
        return self.avg_salary > other.avg_salary

    def __str__(self) -> str:
        salary_info = ""
        if self.__salary["from"] or self.__salary["to"]:
            salary_info = f"{self.__salary['from']}-{self.__salary['to']} {self.__salary['currency']}"
        else:
            salary_info = "Зарплата не указана"

        return (
            f"Вакансия: {self.__title}\n"
            f"Компания: {self.__employer}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self.__description[:100]}...\n"
            f"Ссылка: {self.__link}\n"
            "----------------------------------"
        )

    @staticmethod
    def cast_to_object_list(vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
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