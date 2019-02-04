# -*- coding: utf-8 -*-
from Checker.Api.ApiDA import ApiDA, AuthTypes


class PullRequestsStates:
    OPEN = 'open'
    CLOSED = 'closed'


class GitHub(ApiDA):
    """
    Класс для работы c Rest Api гитхаба
    """

    def __init__(self, urls):
        super().__init__(urls)
        self.token = "no token"
        self.service_url = urls.github

    def get_branches_list(self, expected_status=200):
        """
        Получает список веток репозитория
        :param expected_status:
        :return:
        """
        resp = self._call_service_method(
            'get', '/repos/ursusrepublic/django_test/branches', auth_type=AuthTypes.WITHOUT_AUTH)
        resp_json = self.response_checker(resp, expected_status)
        return resp_json

    def get_pull_requests_list(self, state, expected_status=200):
        """
        Получает список пулл реквестов
        :return:
        """
        params = {'state': state}
        resp = self._call_service_method(
            'get', '/repos/ursusrepublic/django_test/pulls', params=params, auth_type=AuthTypes.WITHOUT_AUTH)
        resp_json = self.response_checker(resp, expected_status)
        return resp_json

    # Так как во всех методах выше работаем только с одним репозиторием, овнера и имя репозитория в качестве параметров
    # не передаю

    def create_issue(self, issue_data, expected_status=201):
        """
        Создает issue
        :return:
        """
        params = {'title': issue_data}
        resp = self._call_service_method(
            'post', '/repos/ramriddick/autotests_web/issues', json=params, auth_type=AuthTypes.TOKEN)
        resp_json = self.response_checker(resp, expected_status)
        return resp_json
