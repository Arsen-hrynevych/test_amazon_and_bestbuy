import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from conftest import driver


@pytest.mark.parametrize("url, search_locator, products_locator", [
    ("https://www.amazon.com/", "//input[@name = 'field-keywords']", "//div[@class = 'a-section']"),
    ("https://www.bestbuy.com/", "//input[@class = 'search-input']", "//div[@class = 'embedded-badge']")])
def test_shopping(driver, url, search_locator, products_locator):
    product = 'samsung galaxy s22'
    driver.get(url)

    if url == "https://www.bestbuy.com/":
        driver.find_element(By.XPATH, '//a[@class = "us-link"]').click()

    search_nav = driver.find_element(By.XPATH, search_locator)
    search_nav.send_keys(product)
    search_nav.send_keys(Keys.RETURN)  # for windows need to be changed to Keys.ENTER

    names_product = driver.find_elements(By.XPATH, products_locator)
    assert len(names_product) != 0, "Page with product isn't displayed"

    # once script completed the line below should be uncommented.
    # assert amazon_price > bestbuy_price
