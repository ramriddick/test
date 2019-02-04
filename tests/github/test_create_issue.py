# -*- coding: utf-8 -*-
from Checker import helpers
helpers.check_pytest(__file__)


def test_create_issue(api):
    """
    - Вызывает метод создания issue
    - Проверяет, что вернулся верный ответ
    """
    issue_title = "found a bug"
    issue_data = api.github.create_issue(issue_title)
    assert issue_data.get("title") == issue_title, "Неправильный ответ сервиса."
