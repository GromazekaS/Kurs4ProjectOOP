import psycopg2
import time
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    """Создает базу данных и таблицы (без удаления существующей БД)"""

    # Флаг для отслеживания, создавалась ли база данных
    db_created = False

    # Сначала попробуем подключиться к существующей базе данных
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.close()
        print(f"База данных {DB_NAME} уже существует.")
    except OperationalError:
        # Если базы не существует, создаем её
        print(f"База данных {DB_NAME} не существует, создаем...")

        # Подключаемся к системной базе данных postgres для создания новой БД
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Создание базы данных
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME} WITH ENCODING 'UTF8'")
            print(f"База данных {DB_NAME} успешно создана.")
            db_created = True
        except psycopg2.errors.DuplicateDatabase:
            print(f"База данных {DB_NAME} уже существует (возможно, создана параллельно).")

        cursor.close()
        conn.close()

    # В любом случае подключаемся к базе данных для создания таблиц
    create_tables()


def create_tables():
    """Создает таблицы в базе данных (если их нет)"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True

        with conn.cursor() as cursor:
            # Проверяем существование таблицы employers
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name = 'employers'
                );
            """)
            employers_exists = cursor.fetchone()[0]

            if not employers_exists:
                cursor.execute("""
                    CREATE TABLE employers (
                        employer_id SERIAL PRIMARY KEY,
                        hh_id INTEGER UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255),
                        description TEXT,
                        vacancies_url VARCHAR(255)
                    )
                """)
                print("Таблица employers создана.")
            else:
                print("Таблица employers уже существует.")

            # Проверяем существование таблицы vacancies
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name = 'vacancies'
                );
            """)
            vacancies_exists = cursor.fetchone()[0]

            if not vacancies_exists:
                cursor.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        hh_id INTEGER UNIQUE NOT NULL,
                        employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE,
                        title VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(10),
                        url VARCHAR(255) NOT NULL,
                        description TEXT,
                        published_at TIMESTAMP,
                        experience VARCHAR(100),
                        employment VARCHAR(100)
                    )
                """)
                print("Таблица vacancies создана.")
            else:
                print("Таблица vacancies уже существует.")

        print(f"Все таблицы в базе данных {DB_NAME} готовы к использованию.")

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        if conn:
            conn.close()