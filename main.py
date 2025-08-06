from src.external_api import HeadHunterAPI
from src.storage import JSONSaver
from src.utils import filter_vacancies, get_top_vacancies, print_vacancies, sort_vacancies
from src.vacancy import Vacancy


def user_interaction():
    """Функция взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    saver = JSONSaver()

    # Ввод данных пользователем
    search_query = input("Введите поисковый запрос (например: Python): ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()

    # Получение данных с API
    vacancies_data = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(vacancies_data)

    # Сохранение в файл
    for vacancy in vacancies_list:
        saver.add_vacancy(vacancy)

    # Фильтрация и сортировка
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод результатов
    print(f"\nНайдено вакансий: {len(vacancies_list)}")
    print(f"Отфильтровано вакансий: {len(filtered_vacancies)}")
    print(f"\nТоп-{top_n} вакансий по зарплате:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
