import os
import time
import json
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class TopsSpider(scrapy.Spider):
    name = "tops_spider"
    allowed_domains = ["tops.co.th"]
    start_urls = ["https://www.tops.co.th/en"]
    
    def create_webdriver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        return webdriver.Chrome(options=options)

    def accept_cookies(self, driver):
        """Handles cookie pop-ups if present."""
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")
            ))
            cookie_button.click()
            self.logger.info("Cookies accepted!")
        except Exception:
            pass
        self.close_popup(driver)

    def close_popup(self, driver):
        """Handles unexpected pop-ups if present."""
        try:
            popup_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]"))
            )
            popup_button.click()
            self.logger.info("Pop-up closed!")
        except Exception:
            pass

    def parse(self, response):
        """Extracts main categories."""
        main_categories = response.css("div.pc-sidenavbar div.item.sidebar-item a::attr(href)").getall()

        for category_url in main_categories:
            yield response.follow(
                category_url, callback=self.parse_subcategories,
                meta={'main_category': category_url.split("/")[-1].replace("-", " ").title()}
            )

    def parse_subcategories(self, response):
        """Extracts all subcategories."""
        driver = self.create_webdriver()
        driver.get(response.url)
        self.accept_cookies(driver)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.tabsPanel div.categories div.ais-RefinementList ul"))
            )
            sub_categories = driver.find_elements(By.CSS_SELECTOR, "li.ais-RefinementList-item a")
            main_category = response.meta['main_category']

            for sub_category in sub_categories:
                sub_category_name = sub_category.text.strip()
                if not sub_category_name:
                    continue

                yield scrapy.Request(
                    url=sub_category.get_attribute("href"),
                    callback=self.scrape_products,
                    meta={'main_category': main_category, 'sub_category': sub_category_name}
                )
        finally:
            driver.quit()

    def scrape_products(self, response):
        """Scrape all products in a subcategory."""
        driver = self.create_webdriver()
        driver.get(response.url)
        self.accept_cookies(driver)

        try:
            self.scroll_page(driver)
            products = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.hits ol.ais-InfiniteHits-list li a"))
            )
            for product in products:
                yield response.follow(
                    product.get_attribute("href"), self.parse_product_details,
                    meta={**response.meta, 'product_url': product.get_attribute("href")}
                )
        finally:
            driver.quit()

    def parse_product_details(self, response):
        """Extracts product details."""
        driver = self.create_webdriver()
        driver.get(response.url)
        self.accept_cookies(driver)

        product = {
            "product_url": response.meta.get("product_url", response.url),
            "name": self.get_element_text(driver, "//h1"),
            "images": [img.get_attribute("href") for img in driver.find_elements(By.XPATH, "//div[contains(@class,'img-zoom-container')]//a")],
            "quantity": self.get_element_text(driver, "//h1").split()[-1],
            "barcode": self.get_element_text(driver, "//div[contains(text(),'SKU')]").replace("SKU", "").strip(),
            "details": self.get_element_text(driver, "//div[contains(@class,'accordion-body')]").strip(),
            "price": self.get_element_text(driver, "//span[contains(@class,'product-Details-current-price')]").strip(),
            "labels": self.get_element_text(driver, "//p[contains(@class,'product-Details-seasonal-label')]").strip()
        }

        driver.quit()
        yield {response.meta['main_category']: {"subcategories": {response.meta['sub_category']: {"products": [product]}}}}

    def get_element_text(self, driver, xpath):
        """Helper function to safely extract element text."""
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except NoSuchElementException:
            return ""

    def scroll_page(self, driver, pause_time=2, step=80):
        """Gradually scrolls the page until reaching the bottom."""
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            for pos in range(0, last_height, step):
                driver.execute_script(f"window.scrollTo(0, {pos});")
                time.sleep(0.5)
            time.sleep(pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
