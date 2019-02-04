# -*- coding: utf-8 -*-


class PageObject:
    """
    Класс для работы с браузером
    """

    def __init__(self, driver, urls):
        self.__driver = driver
        self.__urls = urls

    @property
    def ya(self):
        from Checker.PageObject.Ya import Ya
        return Ya(self.__driver, self.__urls)
