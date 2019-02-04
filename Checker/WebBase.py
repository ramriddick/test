# -*- coding: utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from Checker import MAX_WAIT_TIME, TIMEOUT_STEP


class WebBase(object):

    def __init__(self):
        self.driver = None
        self.settings = None
        self.elem = None

    def __custom_find_by(self, selenium_method, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        Кастомная обертка вокруг всех методов find_element_by_ для поддержки таймаутов и поиска невидимых элементов

        :param str selenium_method:
        :param str val:
        :param int timeout:
        :param bool wait_element_visibility:
        :return:
        """
        from Checker.WebElement import WebElement
        driver = self.driver if not isinstance(self, WebElement) else self.elem

        def expected_condition(d):
            prop = getattr(d, selenium_method)
            # получаем список элементов
            time.sleep(TIMEOUT_STEP)
            elems = prop(val)
            # если элементов не нашлось вообще, то падаем и пробуем опять
            if not elems:
                raise NoSuchElementException
            for el in elems:
                # если элемент уже имеется и видимый, то сразу же вернем его и выйдем
                if el.is_displayed():
                    return el
                # если видимость и не нужна, то сразу же возвращаем этот элемент
                if not wait_element_visibility:
                    return el
                # если элемент это поле для выбора файла, то вернем даже если оно скрыто
                type_attribute = el.get_attribute('type')
                if type_attribute and str(type_attribute).lower().strip() == "file":
                    return el
            # найти ничего не удалось. Падаем и пробуем опять.
            raise NoSuchElementException

        wait = WebDriverWait(driver, timeout, TIMEOUT_STEP)
        try:
            return WebElement(wait.until(expected_condition), self.driver, self.settings)
        except Exception:
            return None

    def __custom_finds_by(self, selenium_method, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        Кастомная обертка вокруг всех методов find_elements_by_ для поддержки таймаутов и поиска невидимых элементов

        :param str selenium_method:
        :param str val:
        :param int timeout:
        :param bool wait_element_visibility:
        :return:
        """
        from Checker.WebElement import WebElement
        driver = self.driver if not isinstance(self, WebElement) else self.elem

        def expected_condition(d):
            result = []
            prop = getattr(d, selenium_method)
            time.sleep(TIMEOUT_STEP)
            elems = prop(val)
            # если элементов не нашлось вообще, то падаем и пробуем опять
            if not elems:
                raise NoSuchElementException
            for el in elems:
                # если элемент уже имеется и он видимый, то берем его и идем к следующему элементу
                if el.is_displayed():
                    result.append(el)
                    continue
                # если видимость и не нужна, то берем элемент и идем к следующему элементу
                if not wait_element_visibility:
                    result.append(el)
                    continue
                # если элемент это поле для выбора файла, то берем его даже если оно скрыто
                type_attribute = el.get_attribute('type')
                if type_attribute and str(type_attribute).lower().strip() == "file":
                    result.append(el)
            # если найти ничего не удалось, то падаем и пробуем опять
            if not result:
                raise NoSuchElementException
            return result

        wait = WebDriverWait(driver, timeout, TIMEOUT_STEP)
        try:
            ret = []
            elements = wait.until(expected_condition)
            for element in elements:
                ret.append(WebElement(element, self.driver, self.settings))
            return ret
        except Exception:
            return []

    def find_element_by_id(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_id', val, timeout, wait_element_visibility)

    def find_elements_by_id(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_id', val, timeout, wait_element_visibility)

    def find_element_by_xpath(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_xpath', val, timeout, wait_element_visibility)

    def find_elements_by_xpath(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_xpath', val, timeout, wait_element_visibility)

    def find_element_by_link_text(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_link_text', val, timeout, wait_element_visibility)

    def find_elements_by_link_text(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_link_text', val, timeout, wait_element_visibility)

    def find_element_by_partial_link_text(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_partial_link_text', val, timeout, wait_element_visibility)

    def find_elements_by_partial_link_text(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_partial_link_text', val, timeout, wait_element_visibility)

    def find_element_by_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_name', val, timeout, wait_element_visibility)

    def find_elements_by_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_name', val, timeout, wait_element_visibility)

    def find_element_by_tag_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_tag_name', val, timeout, wait_element_visibility)

    def find_elements_by_tag_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_tag_name', val, timeout, wait_element_visibility)

    def find_element_by_class_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_class_name', val, timeout, wait_element_visibility)

    def find_elements_by_class_name(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_class_name', val, timeout, wait_element_visibility)

    def find_element_by_css_selector(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype AtiQA.WebElement.WebElement
        """
        return self.__custom_find_by('find_elements_by_css_selector', val, timeout, wait_element_visibility)

    def find_elements_by_css_selector(self, val, timeout=MAX_WAIT_TIME, wait_element_visibility=True):
        """
        :param str val: Селектор
        :param int timeout: Сколько секунд нужно ждать появления элемента
        :param bool wait_element_visibility: Дожидаться ли, что элемент будет отображен на странице?
        :rtype list[AtiQA.WebElement.WebElement]
        """
        return self.__custom_finds_by('find_elements_by_css_selector', val, timeout, wait_element_visibility)
