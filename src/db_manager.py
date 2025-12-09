import psycopg2
from typing import List, Dict, Any, Optional
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.conn.autocommit = True

    def __del__(self):
        if self.conn:
            self.conn.close()

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, COUNT(v.vacancy_id) AS vacancies_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
                ORDER BY vacancies_count DESC
            """)
            return [{"company": row[0], "vacancies_count": row[1]} for row in cursor.fetchall()]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Получает список всех вакансий с указанием компании, названия, зарплаты и ссылки"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, 
                       COALESCE(v.salary_from, 0) AS salary_from,
                       COALESCE(v.salary_to, 0) AS salary_to,
                       v.currency, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return [{
                "company": row[0],
                "title": row[1],
                "salary_from": row[2],
                "salary_to": row[3],
                "currency": row[4],
                "url": row[5]
            } for row in cursor.fetchall()]

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT AVG((salary_from + salary_to) / 2) 
                FROM vacancies 
                WHERE salary_from > 0 AND salary_to > 0
            """)
            return cursor.fetchone()[0] or 0

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Получает список вакансий с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT title, (salary_from + salary_to) / 2 AS avg_salary, url 
                FROM vacancies 
                WHERE (salary_from + salary_to) / 2 > %s
                ORDER BY avg_salary DESC
            """, (avg_salary,))
            return [{
                "title": row[0],
                "avg_salary": row[1],
                "url": row[2]
            } for row in cursor.fetchall()]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает список вакансий по ключевому слову в названии"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT title, (salary_from + salary_to) / 2 AS avg_salary, url 
                FROM vacancies 
                WHERE title ILIKE %s
                ORDER BY avg_salary DESC
            """, (f'%{keyword}%',))
            return [{
                "title": row[0],
                "avg_salary": row[1],
                "url": row[2]
            } for row in cursor.fetchall()]

    def insert_employer(self, employer_data: Dict[str, Any]) -> None:
        """Добавляет работодателя в БД"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employers (hh_id, name, url, description, vacancies_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (hh_id) DO NOTHING
            """, (
                employer_data.get('id'),
                employer_data.get('name'),
                employer_data.get('alternate_url'),
                employer_data.get('description'),
                employer_data.get('vacancies_url')
            ))

    def insert_vacancy(self, vacancy: 'Vacancy') -> None:
        """Добавляет вакансию в БД"""
        with self.conn.cursor() as cursor:
            # Сначала находим employer_id в таблице employers по hh_id
            cursor.execute("""
                SELECT employer_id FROM employers 
                WHERE hh_id = %s
            """, (vacancy.employer_id,))

            result = cursor.fetchone()
            if result is None:
                print(
                    f"Предупреждение: Работодатель с hh_id={vacancy.employer_id} не найден. Вакансия '{vacancy.title}' пропущена.")
                return

            employer_id_in_db = result[0]

            # Теперь вставляем вакансию с найденным employer_id
            cursor.execute("""
                INSERT INTO vacancies (
                    hh_id, employer_id, title, salary_from, salary_to, 
                    currency, url, description, published_at, experience, employment
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (hh_id) DO NOTHING
            """, (
                vacancy.hh_id,
                employer_id_in_db,
                vacancy.title,
                vacancy.salary_from,
                vacancy.salary_to,
                vacancy.currency,
                vacancy.link,
                vacancy.description,
                vacancy.published_at,
                vacancy.experience,
                vacancy.employment
            ))

    def to_db_format_without_employer_id(self) -> tuple:
        """Возвращает данные в формате для вставки в БД без employer_id"""
        return (
            self.__hh_id,
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