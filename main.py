from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.database import create_database
from src.db_manager import DBManager
import time
from typing import List

def user_interaction_db():
    """Интерфейс для работы с базой данных"""
    db = DBManager()

    while True:
        print("\n" + "=" * 50)
        print("Меню работы с базой данных вакансий")
        print("=" * 50)
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "0":
            break

        elif choice == "1":
            companies = db.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for company in companies:
                print(f"{company['company']}: {company['vacancies_count']} вакансий")

        elif choice == "2":
            vacancies = db.get_all_vacancies()
            print("\nВсе вакансии:")
            for vac in vacancies:
                salary = f"{vac['salary_from']}-{vac['salary_to']} {vac['currency']}"
                print(f"{vac['company']} - {vac['title']} - {salary} - {vac['url']}")

        elif choice == "3":
            avg_salary = db.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f} RUB")

        elif choice == "4":
            vacancies = db.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vac in vacancies:
                print(f"{vac['title']} - {vac['avg_salary']:.2f} RUB - {vac['url']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db.get_vacancies_with_keyword(keyword)
            print(f"\nРезультаты поиска по '{keyword}':")
            for vac in vacancies:
                print(f"{vac['title']} - {vac['avg_salary']:.2f} RUB - {vac['url']}")

        else:
            print("Неверный ввод, попробуйте снова")


def load_data_to_db(employer_ids: List[str]):
    """Загружает данные о компаниях и вакансиях в БД"""
    api = HeadHunterAPI()
    db = DBManager()

    # Сначала очистим старые данные, чтобы избежать дублирования
    clear_old_data = input("Очистить старые данные перед загрузкой? (y/n): ").lower()
    if clear_old_data == 'y':
        clear_tables(db)

    for employer_id in employer_ids:
        print(f"Обработка компании с ID: {employer_id}")

        # Получение и сохранение данных о компании
        employer_data = api.get_employer(employer_id)
        if employer_data:
            db.insert_employer(employer_data)
            print(f"Добавлен работодатель: {employer_data.get('name')}")
        else:
            print(f"Не удалось получить данные для работодателя с ID: {employer_id}")
            continue

        # Получение и сохранение вакансий компании
        vacancies_data = api.get_employer_vacancies(employer_id)
        if vacancies_data:
            vacancies = Vacancy.cast_to_object_list(vacancies_data)

            vacancies_count = 0
            for vacancy in vacancies:
                db.insert_vacancy(vacancy)
                vacancies_count += 1

            print(f"Добавлено вакансий: {vacancies_count} для {employer_data.get('name')}")
        else:
            print(f"Нет вакансий для {employer_data.get('name')}")

        time.sleep(0.5)  # Для соблюдения лимитов API

def clear_tables(db: DBManager):
    """Очищает таблицы от старых данных"""
    with db.conn.cursor() as cursor:
        cursor.execute("DELETE FROM vacancies")
        cursor.execute("DELETE FROM employers")
    db.conn.commit()
    print("Старые данные очищены.")


if __name__ == "__main__":
    # Список ID интересных компаний (пример)
    TOP_COMPANIES = [
        '1740',  # Яндекс
        '3529',  # Сбер
        '78638',  # Тинькофф
        '2748',  # Ростелеком
        '3776',  # МТС
        '41862',  # VK
        '87021',  # Wildberries
        '49357',  # Билайн
        '1122462',  # Сбермаркет
        '1057',  # Касперский
    ]

    # Создание базы данных и таблиц
    create_database()

    # Спрашиваем пользователя о загрузке данных
    load_data = input("Хотите загрузить данные о компаниях и вакансиях? (y/n): ").lower()

    if load_data == 'y':
        print("Начинаем загрузку данных...")
        load_data_to_db(TOP_COMPANIES)
        print("\nДанные успешно загружены в базу данных!")
    else:
        print("Используем существующие данные в базе.")

    # Запуск интерфейса пользователя
    user_interaction_db()