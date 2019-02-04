# -*- coding: utf-8 -*-
from Checker.PageObject.Yandex import Yandex


class Ya:
    """
    Класс для работы со страницей ya.ru
    """

    # Заголовок страницы
    title = "Яндекс"

    # Элементы на странице
    search_btn                 = ".search2__button>button"
    search_input               = ".search2__input .input__input"
    yandex_link                = "a[href='//yandex.ru']"


    def __init__(self, driver, urls):
        self.__driver = driver
        self.__urls = urls

    def get_ya_page(self):
        """
        Переходим на страницу ya.ru

        :return:
        """
        self.__driver.get(self.__urls.ya)

    def check_title(self):
        """
        Проверяет тайтл
        :return:
        """
        assert self.__driver.wait_for_title(self.title), """Тайтл не совпадает с ожидаемым.
        отобразился: {0}
        ожидался: {1}""".format(self.__driver.title, self.title)

    def fill_search_input(self, search_data):
        """
        Заполняет инпут поиска
        :param search_data:
        :return:
        """
        search_input = self.__driver.find_element_by_css_selector(self.search_input)
        search_input.fill(search_data)

    def search_btn_click(self):
        """
        Кликает на кнопку поиска.
        :return:
        """
        search_btn = self.__driver.find_element_by_css_selector(self.search_btn)
        search_btn.click()
        return Yandex(self.__driver, self.__urls)
