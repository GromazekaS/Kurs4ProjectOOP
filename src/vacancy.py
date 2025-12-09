from typing import Dict, Any, Optional, List


class Vacancy:
    __slots__ = (
        '__hh_id', '__title', '__link', '__salary_from',
        '__salary_to', '__currency', '__description',
        '__employer_id', '__published_at', '__experience',
        '__employment'
    )

    def __init__(
            self,
            hh_id: int,
            title: str,
            link: str,
            salary: Optional[Dict[str, Any]],
            description: str,
            employer_id: int,
            published_at: str,
            experience: Optional[Dict[str, str]],
            employment: Optional[Dict[str, str]]
    ) -> None:
        self.__hh_id: int = hh_id
        self.__title: str = title
        self.__link: str = link
        self.__salary_from, self.__salary_to, self.__currency = self.__validate_salary(salary)
        self.__description: str = description
        self.__employer_id: int = employer_id
        self.__published_at: str = published_at
        self.__experience: str = experience.get('name') if experience else "Не указан"
        self.__employment: str = employment.get('name') if employment else "Не указан"

    def __validate_salary(
            self,
            salary_data: Optional[Dict[str, Any]]
    ) -> tuple[int, int, str]:
        if not salary_data:
            return 0, 0, "не указана"

        salary_from = salary_data.get("from") or 0
        salary_to = salary_data.get("to") or 0
        currency = salary_data.get("currency", "RUR")

        return salary_from, salary_to, currency

    @property
    def hh_id(self) -> int:
        return self.__hh_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    @property
    def salary_from(self) -> int:
        return self.__salary_from

    @property
    def salary_to(self) -> int:
        return self.__salary_to

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def description(self) -> str:
        return self.__description

    @property
    def employer_id(self) -> int:
        return self.__employer_id

    @property
    def published_at(self) -> str:
        return self.__published_at

    @property
    def experience(self) -> str:
        return self.__experience

    @property
    def employment(self) -> str:
        return self.__employment

    @property
    def avg_salary(self) -> float:
        if self.__salary_from and self.__salary_to:
            return (self.__salary_from + self.__salary_to) / 2
        return self.__salary_from or self.__salary_to or 0

    def __lt__(self, other: 'Vacancy') -> bool:
        return self.avg_salary < other.avg_salary

    def __gt__(self, other: 'Vacancy') -> bool:
        return self.avg_salary > other.avg_salary

    def to_db_format(self) -> tuple:
        """Возвращает данные в формате для вставки в БД"""
        return (
            self.__hh_id,
            self.__employer_id,
            self.__title,
            self.__salary_from,
            self.__salary_to,
            self.__currency,
            self.__link,
            self.__description,
            self.__published_at,
            self.__experience,
            self.__employment
        )

    def __str__(self) -> str:
        salary_info = ""
        if self.__salary_from or self.__salary_to:
            salary_info = f"{self.__salary_from}-{self.__salary_to} {self.__currency}"
        else:
            salary_info = "Зарплата не указана"

        return (
            f"Вакансия: {self.__title}\n"
            f"Тип занятости: {self.__employment}\n"
            f"Опыт: {self.__experience}\n"
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
                hh_id=item.get("id"),
                title=item.get("name", "Без названия"),
                link=item.get("alternate_url", "#"),
                salary=item.get("salary"),
                description=item.get("snippet", {}).get("requirement", ""),
                employer_id=item.get("employer", {}).get("id"),
                published_at=item.get("published_at", ""),
                experience=item.get("experience"),
                employment=item.get("employment")
            )
            vacancies.append(vacancy)
        return vacancies