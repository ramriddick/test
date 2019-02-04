# -*- coding: utf-8 -*-
from Checker.Api.GitHub import GitHub


class Api:
    """
    Класс для работы с апи
    """
    def __init__(self, urls):
        self.__urls = urls
        self.__github = GitHub(self.__urls)

    @property
    def github(self):
        """
        :return:
        """
        return self.__github
