# -*- coding: utf-8 -*-


class Urls:
    github = ''
    ya = ''


    def __init__(self, config_urls):
        for el in config_urls:
            if not hasattr(self, el):
                raise Exception("Передали неизвестный для класса Urls аттрибут '" + el + "'")
            setattr(self, el, config_urls[el])
