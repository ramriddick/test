# -*- coding: utf-8 -*-
import pytest
from Checker import helpers
from Checker.Api.GitHub import PullRequestsStates
helpers.check_pytest(__file__)


@pytest.mark.parametrize('request_state', [PullRequestsStates.CLOSED, PullRequestsStates.OPEN])
def test_get_opened_closed_requests(api, request_state):
    """
    - Получает список закрытых/открытых пулл реквестов
    - Проверяет, что вернулся список и он не пуст
    """
    closed_requests = api.github.get_pull_requests_list(request_state)
    assert closed_requests and type(closed_requests)==list, "Неправильный ответ сервиса. Ожидался непустой список"
