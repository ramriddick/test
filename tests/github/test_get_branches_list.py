# -*- coding: utf-8 -*-
from Checker import helpers
helpers.check_pytest(__file__)


def test_get_branches_list(api):
    """
    - Получает список веток репозитория
    - Проверяет, что вернулся список и он не пуст
    """
    branches_list = api.github.get_branches_list()
    assert branches_list and type(branches_list)==list, "Неправильный ответ сервиса. Ожидался непустой список"
