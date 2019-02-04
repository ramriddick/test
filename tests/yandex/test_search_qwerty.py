# -*- coding: utf-8 -*-
from Checker import helpers
helpers.check_pytest(__file__)


def test_search_qwerty(page_object):
    """
    Проверка формы поиска на странице ya.ru

    - Открывает страницу ya.ru
    - Заполняет форму поиска
    - Нажимает на кнопку поиска
    - Проверяет, что на странице поиска в строке поиска правильные данные
    """
    search_data = 'qwerty'

    ya_page = page_object.ya
    ya_page.get_ya_page()
    ya_page.check_title()
    ya_page.fill_search_input(search_data)
    assert False

    yandex_search_page = ya_page.search_btn_click()
    yandex_search_page.check_data_in_input_search(search_data)
