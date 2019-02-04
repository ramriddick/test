# -*- coding: utf-8 -*-
from Checker.WebBase import WebBase


class WebElement(WebBase):
    """
    Базовые манипуляции с элементами
    """

    def __init__(self, elem, driver, settings):
        super().__init__()
        self.elem = elem
        self.driver = driver
        self.settings = settings

    def __getattr__(self, attr):
        prop = getattr(self.elem, attr)
        return prop

    def click(self):
        """
        Кликнуть по элементу

        :return:
        """
        element = self.elem
        assert element, "Елемент не найден, либо невидимый"
        self.elem.click()
        return self

    def fill(self, text):
        """
        Ввести в текстовое поле значение

        :param text:
        :return:
        """
        self.elem.click()
        self.elem.send_keys(text)

        return self
