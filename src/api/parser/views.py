from flask import Blueprint, jsonify

from src.api.parser.models import Category, SubCategory, Product
from src.utils.parser.html_handler import SubCategoryParser, HtmlHandler

parser_api = Blueprint("parser_api", __name__)


@parser_api.route("/", methods=["GET"])
def start_page():
    return jsonify("It works!")


@parser_api.route("/category/parse", methods=["GET"])
def parse_categories():
    for category in HtmlHandler().categories:
        db_category = Category.create(name=category.name, url=category.url)
        subcategories = category.subcategories
        for subcategory in subcategories:
            SubCategory.create(name=subcategory.name, url=subcategory.url, category=db_category)
    return jsonify([Category.to_dict(category) for category in Category.get_all()])


@parser_api.route("/category", methods=["GET"])
def get_all_categories():
    return jsonify([Category.to_dict(cat) for cat in Category.get_all()])


@parser_api.route("/category/<int:id>", methods=["GET"])
def get_category_by_id(id):
    category = Category.get(id)
    if not category:
        return jsonify("Not Found"), 404
    return jsonify(Category.to_dict(category))


@parser_api.route("/category/<int:id>/parse_products", methods=["GET"])
def parse_category_by_id(id):

    category = Category.get(id)
    if not category:
        return jsonify("Not Found"), 404

    for subcategory in category.subcategories:
        sc_parse = SubCategoryParser(url=subcategory.url)

        products = []
        for product_sublist in sc_parse.products():
            for product in product_sublist:
                products.append(product)

        for product in products:
            product["sku_category"] = f"{category.name}/{subcategory.name}"
            Product.create(
                price_datetime=product.get("price_datetime"),
                price=product.get("price"),
                price_promo=product.get("price_promo"),
                sku_status=product.get("sku_status"),
                sku_barcode=product.get("sku_barcode"),
                sku_article=product.get("sku_article"),
                sku_name=product.get("sku_name"),
                sku_category=product.get("sku_category"),
                sku_country=product.get("sku_country"),
                sku_weight_min=product.get("sku_weight_min"),
                sku_volume_min=product.get("sku_volume_min"),
                sku_quantity_min=product.get("sku_quantity_min"),
                sku_images=product.get("sku_images"),
                subcategory=subcategory,
            )
    return jsonify(Category.to_dict(category))
