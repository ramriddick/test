# -*- coding: utf-8 -*-
import sys

import datetime
import pytest
import os

from Checker import SCREENSHOTS_PATH
from Checker.Api import Api
from Checker.Config import Config
from Checker.PageObject import PageObject
from Checker.Urls import Urls
from Checker.WebDriver import WebDriver


def pytest_configure():
    sys._called_from_test = True


def pytest_unconfigure():
    del sys._called_from_test


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Лайв-хак, который позволит всем фикстурам при окончании работы узнать о статусе прохождения теста
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "report", rep)
    return rep

@pytest.fixture(scope="session")
def config():
    """
    Конфигурация
    :return Config:
    """
    config = Config(os.path.dirname(os.path.abspath(__file__)))
    return config


@pytest.fixture(scope="session")
def urls(config):
    return Urls(config["urls"])


@pytest.fixture(scope='session')
def api(urls):
    """
    Класс для работы с api
    :return Api:
    """
    return Api(urls)


@pytest.fixture(scope="class")
def _driver(request, config):
    """
    Кастомный WebDriver
    :param request:
    :return WebDriver:
    """
    wb = WebDriver(config)

    def fin():
        wb.close()
        wb.quit()

    request.addfinalizer(fin)
    return wb


@pytest.fixture(scope="class")
def driver(request, _driver):
    """
    Обертка вокруг нашего драйвера, которая выполняется каждый запуск теста.
    :return:
    """
    def check_test_status():
        failed = None
        if hasattr(request.node, "report"):
            failed = request.node.report.failed

        if not failed:
            return

        # тест упал, самое время попробовать сделать скриншот
        if not _driver:
            return
        try:
            # Сделаем скриншот
            if not os.path.isdir(SCREENSHOTS_PATH):
                os.mkdir(SCREENSHOTS_PATH)
            _driver.save_screenshot(os.path.join(
                SCREENSHOTS_PATH, request.node.name + datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S') +'.png'))
        except Exception:
            pass

    def fin():
        check_test_status()

    request.addfinalizer(fin)
    return _driver


@pytest.fixture(scope='class')
def page_object(driver, urls):
    """
    Объект для работы с Page Object

    :param urls:
    """
    return PageObject(driver, urls)
