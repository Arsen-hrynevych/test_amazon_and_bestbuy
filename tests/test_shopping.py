import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from conftest import driver


@pytest.mark.parametrize("url, search_locator, products_locator, price_locator, review_locator ", [
    ("https://www.amazon.com/", "//input[@name = 'field-keywords']", "//div[@class = 'a-section']",
     "span.a-price-whole", "span.a-size-base.s-underline-text"),
    ("https://www.bestbuy.com/", "//input[@class = 'search-input']", "//div[@class = 'embedded-badge']",
     "div.priceView-hero-price span:first-child", "span.c-reviews")])
def test_shopping(driver, url, search_locator, products_locator, price_locator, review_locator, ):
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

    max_review = 0
    min_price = 0
    bestbuy_price = 0
    amazon_price = 0

    for i in range(len(products_price)):
        if i >= len(review_counts):
            break

        review_count_text = review_counts[i].text.strip('()').replace(',', '')

        if review_count_text == '':
            break

        if '$' in review_count_text:
            review_count_text = review_count_text.replace('$', '')
        try:
            review_count = int(float(review_count_text))
        except:
            continue

        if review_count > max_review:
            max_review = review_count
            min_price = products_price[i].text.replace(',', '')

        if "amazon" in url and min_price != '':
            amazon_price = float(min_price)
        if "best" in url:
            bestbuy_price = float(min_price.replace('$', ''))
    # once script completed the line below should be uncommented.
    assert amazon_price > bestbuy_price
