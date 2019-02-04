# -*- coding: utf-8 -*-
import json
from requests import Response


class ServiceApiError(Exception):
    def __init__(self, value, reason=None):
        self.value = value
        self.reason = reason
        self.json = self.format_exception()

    def __str__(self):
        msg_text = json.dumps(self.json, indent=6, separators=(',', ': '), ensure_ascii=False)
        return msg_text

    def format_exception(self):
        if not isinstance(self.value, Response):
            return

        exception_data = {
            "request":
                {
                    "body": self.get_request_body(),
                    "headers": dict(self.value.request.headers),
                    "method": str(self.value.request.method),
                    "url": str(self.value.request.url)
                },
            "response":
                {
                    "headers": dict(self.value.headers),
                    "http_status": int(self.value.status_code),
                    "body": self.get_response_body()
                }
        }
        if self.reason:
            exception_data['reason'] = self.reason
        return exception_data

    def get_response_body(self):
        try:
            response_body = self.value.json()
        except ValueError:
            response_body = self.value.text
        return response_body

    def get_request_body(self):
        if not self.value.request.body:
            return
        try:
            request_body = self.value.request.body.decode("utf-8")
        except Exception:
            return "Не удалось распарсить тело запроса"
        converted_request_body = json.loads(request_body)
        return converted_request_body
