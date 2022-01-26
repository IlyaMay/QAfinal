from .pages.product_page import ProductPage
from .pages.login_page import LoginPage
from .pages.basket_page import BasketPage

import pytest
import time

basic_product_url = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/coders-at-work_207/"


@pytest.mark.skip(reason='parametrization is out of final project')
@pytest.mark.parametrize('offer_number',
                         [*range(7), pytest.param(7, marks=pytest.mark.xfail(reason='bugged link')), *range(8, 10)])
def test_guest_can_add_product_to_basket(browser, offer_number):
    link = f"{basic_product_url}?promo=offer{offer_number}"
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.add_to_basket()
    product_page.solve_quiz_and_get_code()
    product_page.should_be_correct_addition_to_basket()


@pytest.mark.login_guest
class TestLoginFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.link = basic_product_url
        self.product_page = ProductPage(browser, self.link)

    def test_guest_should_see_login_link_on_product_page(self, browser):
        self.product_page.open()
        self.product_page.should_be_login_link()

    @pytest.mark.need_review
    def test_guest_can_go_to_login_page_from_product_page(self, browser):
        self.product_page.open()
        self.product_page.go_to_login_page()
        login_page = LoginPage(browser, browser.current_url)
        login_page.should_be_login_page()


@pytest.mark.basket_user
class TestUserAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.link = basic_product_url
        self.product_page = ProductPage(browser, self.link)
        self.product_page.open()
        self.product_page.go_to_login_page()
        login_page = LoginPage(browser, browser.current_url)
        email = str(time.time()) + "@fakemail.org"
        password = str(time.time()) + "+password"
        login_page.register_new_user(email, password)
        login_page.should_be_success_message()
        login_page.should_be_authorized_user()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        self.product_page.open()
        self.product_page.add_to_basket()
        self.product_page.should_be_correct_addition_to_basket()

    def test_user_cant_see_success_message(self, browser):
        self.product_page.open()
        self.product_page.should_not_be_success_message()


@pytest.mark.basket_guest
class TestGuestAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.link = basic_product_url
        self.product_page = ProductPage(browser, self.link)

    def test_guest_cant_see_success_message(self, browser):
        self.product_page.open()
        self.product_page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_guest_cant_see_product_in_basket_opened_from_product_page(self, browser):
        self.product_page.open()
        self.product_page.go_to_basket_page()
        basket_page = BasketPage(browser, browser.current_url)
        basket_page.should_be_basket_page()
        basket_page.should_be_empty_basket()
        basket_page.should_be_empty_basket_message()

    @pytest.mark.need_review
    def test_guest_can_add_product_to_basket(self, browser):
        self.product_page.open()
        self.product_page.add_to_basket()
        self.product_page.should_be_correct_addition_to_basket()

    @pytest.mark.xfail(reason='negative check')
    def test_guest_cant_see_success_message_after_adding_product_to_basket(self, browser):
        self.product_page.open()
        self.product_page.add_to_basket()
        self.product_page.should_not_be_success_message()

    @pytest.mark.xfail(reason='negative check')
    def test_message_disappeared_after_adding_product_to_basket(self, browser):
        self.product_page.open()
        self.product_page.add_to_basket()
        self.product_page.success_message_should_be_disappeared()
