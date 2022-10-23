import os
import urllib.parse
from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv

from src.utils.parser.utils import ParserUtils

load_dotenv()

PARSE_URL = os.getenv("PARSE_URL")
PARSE_FEATURE = os.getenv("PARSE_FEATURE") or "lxml"


class CategoryParser:
    def __init__(self, url):
        self.url = url
        self.name = self.get_name()

    def html_soup(self):
        return BeautifulSoup(
            markup=ParserUtils.get_html(url=urllib.parse.urljoin(PARSE_URL, self.url)), features=PARSE_FEATURE
        )

    def get_name(self):
        name = self.html_soup().find("div", class_="catalog-info-center").find("h1").text
        return name.strip()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def subcategories(self):
        subcategories = self.html_soup().find("ul", class_="catalog-menu-left-1").find_all("a", class_="item-depth-1")
        urls = [sc["href"] for sc in subcategories]
        return [SubCategoryParser(url) for url in urls]


class SubCategoryParser:
    def __init__(self, url):
        self.url = url
        self.base_url = PARSE_URL
        self.name = self.get_name()

    def html_soup(self):
        return BeautifulSoup(
            markup=ParserUtils.get_html(url=urllib.parse.urljoin(PARSE_URL, self.url)), features=PARSE_FEATURE
        )

    def get_name(self):
        name = self.html_soup().find("ul", class_="breadcrumb-navigation").find("li", class_="last").text
        return name.strip()

    def __repr__(self):
        return self.name

    def get_html_soup_by_url(self, url):
        url = urllib.parse.urljoin(self.base_url, url)
        return BeautifulSoup(ParserUtils.get_html(url=url), features=PARSE_FEATURE)

    def products(self):
        html_soup = self.get_html_soup_by_url(self.url)
        goods = html_soup.find("div", class_="catalog-section")
        products_lst = goods.find_all("div", class_="catalog-item first catalog-itemlist") + goods.find_all(
            "div", class_="catalog-item catalog-itemlist"
        )
        page_urls = HtmlHandler.handle_pagination(html_soup)
        if page_urls:
            for page_url in page_urls[1:]:
                products = self.get_products_from_page_by_url(url=page_url)
                products_lst += products
        return [self.get_product_info(pr) for pr in products_lst]

    def get_products_from_page_by_url(self, url):
        html_soup = self.get_html_soup_by_url(url)
        products = html_soup.find("div", class_="catalog-section")
        products_lst = products.find_all("div", class_="catalog-item first catalog-itemlist") + products.find_all(
            "div", class_="catalog-item catalog-itemlist"
        )
        return products_lst

    def get_product_info(self, product: Tag):
        content_info = product.find("div", class_="catalog-content-info")
        content_info_name = content_info.find("a", class_="name")
        sku_name = content_info_name.attrs.get("title")

        url = content_info_name.attrs.get("href")
        html_soup = self.get_html_soup_by_url(url)

        price_datetime = datetime.now()
        articles = html_soup.find("table", class_="tg22 b-catalog-element-offers-table").find_all(
            "tr", class_="b-catalog-element-offer"
        )
        photos = html_soup.find_all("div", class_="catalog-element-small-picture")
        sku_country = html_soup.find("div", class_="catalog-element-offer-left").find("p")
        if sku_country:
            sku_country = sku_country.text.split(": ")[-1]

        sku_images = []
        for photo in photos:
            sku_image = photo.find("a")
            if not sku_image:
                sku_image = html_soup.find("img").attrs.get("src")
            else:
                sku_image = sku_image.attrs.get("href")

            sku_images.append(sku_image)

        articles_list = []
        for article in articles:
            sku_weight_min = ""
            sku_volume_min = ""
            sku_quantity_min = ""
            sku_status = 1

            tr = article.find_all("td")
            if len(tr) < 5:
                continue

            sku_article = tr[0].find_all("b")
            if sku_article:
                sku_article = sku_article[-1].text

            sku_barcode = tr[1].find_all("b")
            if sku_barcode:
                sku_barcode = sku_barcode[-1].text

            size = tr[2].find_all("b")
            if size:
                size = size[-1].text

            if size.endswith("л"):
                sku_volume_min = size[:-1]
            elif size.endswith("кг"):
                sku_weight_min = size[:-2]
            elif size.endswith("г"):
                sku_weight_min = size[:-1]
            elif size.endswith("шт"):
                sku_quantity_min = size[:-2]

            if tr[4].find("s"):
                price = tr[4].find("s")
                if price:
                    price = int(price.text.replace("р", "").replace(" ", ""))

                price_promo = tr[4].find("span")
                if price_promo:
                    price_promo = int(price_promo.text.replace("р", "").replace(" ", ""))
            else:
                price = tr[4].find("span")
                if price:
                    price = int(price.text.replace("р", "").replace(" ", ""))
                price_promo = ""

            if tr[-1].find("catalog-item-no-stock"):
                sku_status = 0

            articles_list.append(
                {
                    "price_datetime": price_datetime,
                    "price": price,
                    "price_promo": price_promo,
                    "sku_status": sku_status,
                    "sku_barcode": sku_barcode,
                    "sku_article": sku_article,
                    "sku_name": sku_name,
                    "sku_country": sku_country,
                    "sku_weight_min": sku_weight_min,
                    "sku_volume_min": sku_volume_min,
                    "sku_quantity_min": sku_quantity_min,
                    "sku_images": sku_images,
                }
            )
        return articles_list


class HtmlHandler:
    def __init__(self, base_url=PARSE_URL):
        self.base_url = base_url
        self.html_soup = BeautifulSoup(markup=ParserUtils.get_html(url=self.base_url), features=PARSE_FEATURE)

    @property
    def categories(self):
        categories = self.html_soup.find("div", id="catalog-menu").find_all("li", class_="lev1")
        urls = [category.find("a", class_="catalog-menu-icon")["href"] for category in categories]
        return [CategoryParser(url) for url in urls]

    @property
    def subcategories(self):
        subcategories = []
        for category in self.categories:
            category_subcategories = category.subcategories
            if category_subcategories:
                subcategories += category_subcategories
        return subcategories

    @staticmethod
    def handle_pagination(soup: BeautifulSoup):
        navigation = soup.find("div", class_="navigation")
        if not navigation:
            return None
        pages = navigation.find_all("a")
        last_page = pages[-1]
        last_page_url = last_page.attrs.get("href")
        lp_lst = last_page_url.split("PAGEN_1=")
        last_page = int(lp_lst[-1])

        url = pages[0].attrs.get("href")

        pagen_index = url.find("PAGEN")
        url_base = url[:pagen_index]
        urls = []
        for i in range(1, last_page + 1):
            urls.append(f"{url_base}PAGEN_1={i}")
        urls = [urllib.parse.urljoin(PARSE_URL, url) for url in urls]

        return urls
