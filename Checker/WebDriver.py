# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Checker import MAX_WAIT_TIME
from Checker.WebBase import WebBase


class WebDriver(WebBase):
    def __init__(self, settings, browser=None, test_name='Unknown'):
        super().__init__()
        self.settings = settings
        self.test_name = test_name
        browser = browser if browser else self.settings.get('browser', 'firefox')
        grid_url = self.settings.get('grid_url', None)
        if self.settings.get('use_grid', False) and grid_url:
            self.driver = self.__remote_driver(grid_url, browser)
        else:
            self.driver = self.__local_driver(browser)
        self.root_window = self.driver.current_window_handle
        self.domain_history = []

    def __getattr__(self, attr):
        prop = getattr(self.driver, attr)
        return prop

    def __local_driver(self, browser='firefox'):
        browser = browser.lower()
        options = self.settings.get('browser_options', None)
        options = options.get(browser, None) if options else None

        if browser == 'firefox':
            profile = webdriver.FirefoxProfile()
            if options:
                for opt, val in options.items():
                    profile.set_preference(opt, val)
            return webdriver.Firefox(profile)
        elif browser == 'chrome':
            profile = webdriver.ChromeOptions()
            profile.add_argument('--disable-internal-flash')
            profile.add_argument('--window-size=1920,1080')
            capabilities = DesiredCapabilities.CHROME
            capabilities['PAGE_LOAD_STRATEGY'] = 'eager'
            if options:
                for opt in options:
                    profile.add_argument(opt)
            desired = profile.to_capabilities()
            desired['loggingPrefs'] = {'browser': 'ALL'}
            maximize_window = self.settings.get('browser_options', None)

            driver = webdriver.Chrome(desired_capabilities=desired)
            if maximize_window:
                driver.set_window_position(0, 0)
                driver.set_window_size(1920, 1080)
            return driver
        elif browser == 'phantomjs':
            driver = webdriver.PhantomJS()
            driver.set_window_size(1024, 768)
            return driver
        else:
            assert hasattr(webdriver, browser.lower()), "Browser {} not supported".format(browser)
            return getattr(webdriver, browser.title())()

    def __remote_driver(self, grid_url, browser='firefox'):
        browser = browser.lower()
        options = self.settings.get('browser_options', None)
        options = options.get(browser, None) if options else None

        if browser == 'firefox':
            profile = webdriver.FirefoxProfile()
            if options:
                for opt, val in options.items():
                    profile.set_preference(opt, val)
            # сохраняем эти настройки для передачи на удаленный браузер
            profile.update_preferences()
            profile.accept_untrusted_certs = True
            caps = DesiredCapabilities.FIREFOX
            caps['firefox_profile'] = profile.encoded
            return webdriver.Remote(command_executor=grid_url, desired_capabilities=caps)
        elif browser == 'chrome':
            profile = webdriver.ChromeOptions()
            profile.add_argument('--disable-internal-flash')
            profile.add_argument('--window-size=1920,1080')
            if options:
                for opt in options:
                    profile.add_argument(opt)
            desired = profile.to_capabilities()
            desired['loggingPrefs'] = {'browser': 'ALL'}
            desired["PAGE_LOAD_STRATEGY"] = "eager"
            return webdriver.Remote(command_executor=grid_url, desired_capabilities=desired)
        else:
            assert hasattr(webdriver, browser.lower()), "Browser {} not supported".format(browser)
            return getattr(webdriver, browser.title())()

    def wait_for_title(self, title, timeout=MAX_WAIT_TIME):
        """
        Ждать появления указанного текста в заголовке страницы
        :param title:
        :param timeout:
        :return:
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.title_contains(title)
            )
        except Exception as e:
            return False
        return True
