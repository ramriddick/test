# -*- coding: utf-8 -*-


class Yandex:
    """
    Класс для работы со страницей https://yandex.ru/search
    """

    # Элементы на странице
    search_input                 = "input[class='input__control']"

    def __init__(self, driver, urls):
        self.__driver = driver
        self.__urls = urls

    def check_data_in_input_search(self, data):
        """
        Проверяем, что в инпуте поиска верное значение

        :return:
        """
        search_input = self.__driver.find_element_by_css_selector(self.search_input)
        value = search_input.get_attribute('value')
        assert value == data, """Текст в строке поиска не совпадает с ожидаемым.
            отобразился: {0}
            ожидался: {1}""".format(value, data)
