# -*- coding: utf-8 -*-
import requests
from urllib3.exceptions import InsecureRequestWarning
from Checker.Api.ServiceApiError import ServiceApiError


class AuthTypes:
    WITHOUT_AUTH = 'without_token'
    TOKEN = 'token'


class ApiDA:
    def __init__(self, urls):
        requests.urllib3.disable_warnings(InsecureRequestWarning)
        self._urls = urls
        self.__service_url = ''
        self.__token = ''

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        if not value:
            pass
        else:
            self.__token = value

    @property
    def service_url(self):
        return self.__service_url

    @service_url.setter
    def service_url(self, value):
        if not value:
            pass
        else:
            self.__service_url = value

    def _call_service_method(
            self, method, url, json=None, params=None, auth_type=None):
        """
        Вызывает метод апи
        """
        # Определяем, по какому адресу стучимся
        url = self._get_url(url)
        # Получаем авторизационные заголовки
        auth_headers = self._get_auth_headers(auth_type)
        auth_headers.update({'Accept': 'application/json'})

        assert hasattr(requests, method.lower()), 'Неизвестный метод ' + method
        req = getattr(requests, method.lower())
        resp = req(url, json=json, params=params, verify=False, headers=auth_headers)
        return resp

    def _get_url(self, url):
        return self.__service_url + url

    def _get_auth_headers(self, auth_type):
        """
        Получает авторизационные заголовки в зависимости от типа авторизации
        :return:
        """
        headers = {}

        if auth_type == AuthTypes.TOKEN:
            headers['Authorization'] = 'token ' + self.token
        elif auth_type == AuthTypes.WITHOUT_AUTH:
            return headers
        else:
            assert False, "Передан неизвестный тип авторизации"
        return headers

    @staticmethod
    def response_checker(resp, expected_status):
        if expected_status:
            if resp.status_code != expected_status:
                raise ServiceApiError(resp, reason="Ожидался статус: {0}".format(expected_status))
        try:
            resp_json = resp.json()
        except ValueError:
            return ''
        return resp_json
