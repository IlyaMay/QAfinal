from .pages.main_page import MainPage
from .pages.login_page import LoginPage
from .pages.basket_page import BasketPage

import pytest

main_page_url = "http://selenium1py.pythonanywhere.com"


@pytest.mark.login_guest
class TestLoginFromMainPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.link = main_page_url
        self.page = MainPage(browser, self.link)

    def test_guest_can_go_to_login_page(self, browser):
        self.page.open()
        self.page.go_to_login_page()
        login_page = LoginPage(browser, browser.current_url)
        login_page.should_be_login_page()

    def test_guest_should_see_login_link(self, browser):
        self.page.open()
        self.page.should_be_login_link()


def test_guest_cant_see_product_in_basket_opened_from_main_page(browser):
    link = main_page_url
    page = MainPage(browser, link)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_basket_page()
    basket_page.should_be_empty_basket()
    basket_page.should_be_empty_basket_message()