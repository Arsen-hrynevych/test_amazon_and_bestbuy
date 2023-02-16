import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from conftest import driver

first_dict = {}
second_dict = {}


@pytest.mark.parametrize("url, search_locator, products_locator, price_locator, review_locator ", [
    ("https://www.amazon.com/", "//input[@name = 'field-keywords']", "//div[@class = 'a-section']",
     "span.a-price-whole", "span.s-underline-text"),
    ("https://www.bestbuy.com/", "//input[@class = 'search-input']", "//div[@class = 'embedded-badge']",
     "div.priceView-hero-price span:first-child", "span.c-reviews")])
def test_shopping(driver, url, search_locator, products_locator, price_locator, review_locator):
    product = 'samsung galaxy s22'

    driver.get(url)

    if url == "https://www.bestbuy.com/":
        driver.find_element(By.XPATH, '//a[@class = "us-link"]').click()

    search_nav = driver.find_element(By.XPATH, search_locator)
    search_nav.send_keys(product)
    search_nav.send_keys(Keys.RETURN)  # for windows need to be changed to Keys.ENTER

    names_product = driver.find_elements(By.XPATH, products_locator)
    assert len(names_product) != 0, "Page with product isn't displayed"

    review_counts = driver.find_elements_by_css_selector(review_locator)
    products_price = driver.find_elements_by_css_selector(price_locator)

    for i in range(len(products_price)):
        if i >= len(review_counts):
            break

        review_count_text = review_counts[i].text.strip('()').replace(',', '.')
        price_count_text = products_price[i + 1].text.strip('$').replace(',', '.')

        if review_count_text == '' or price_count_text == '' or review_count_text == 'Not Yet Reviewed':
            continue

        review_count = int(review_count_text.replace('.', ''))
        price_count = float(price_count_text.replace('.99', ''))

        if "amazon" in url:
            first_dict[review_count] = price_count
        if "bestbuy" in url:
            second_dict[review_count] = price_count

    max_first_value = max(first_dict)
    max_second_value = max(second_dict)
    amazon_price = first_dict[max_first_value]
    bestbuy_price = second_dict[max_second_value]

    # once script completed the line below should be uncommented.

    assert amazon_price > bestbuy_price
