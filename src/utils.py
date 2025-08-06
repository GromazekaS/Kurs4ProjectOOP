from typing import Dict, List, Any, Optional


def filter_vacancies(vacancies: list, filter_words: list) -> list:
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        if vacancy.description: description = vacancy.description.lower()
        else: description = ''
        title = vacancy.title.lower()
        words = " ".join([title, description])

        if all(word.lower() in words for word in filter_words):
            filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: list) -> list:
    """Сортировка вакансий по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Получение топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: list) -> None:
    """Вывод вакансий на экран"""
    if not vacancies:
        print("Вакансии не найдены")
        return

    for vacancy in vacancies:
        print(vacancy)