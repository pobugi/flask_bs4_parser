from src import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    subcategories = db.relationship("SubCategory", back_populates="category")
    created = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get(id):
        return Category.query.get(id)

    @staticmethod
    def create(name, url):
        category = Category(name=name, url=url, created=datetime.now())
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def to_dict(obj):
        return {
            "id": obj.id,
            "name": obj.name,
            "created": obj.created,
            "subcategories": [SubCategory.to_dict(sc) for sc in obj.subcategories],
        }


class SubCategory(db.Model):
    __tablename__ = "subcategory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", back_populates="subcategories")
    products = db.relationship("Product", back_populates="subcategory")
    created = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get(id):
        return SubCategory.query.get(id)

    @staticmethod
    def create(name, url, category):
        subcategory = SubCategory(name=name, url=url, category=category, created=datetime.now())
        db.session.add(subcategory)
        db.session.commit()
        return subcategory

    @staticmethod
    def get_all():
        return SubCategory.query.all()

    @staticmethod
    def to_dict(obj):
        return {
            "id": obj.id,
            "name": obj.name,
            "category_id": obj.category_id,
            "products": [Product.to_dict(pr) for pr in Product.get_all_by_subcategory(subcategory=obj)],
            "created": obj.created,
        }


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    price_datetime = db.Column(db.DateTime)
    price = db.Column(db.String)
    price_promo = db.Column(db.String)
    sku_status = db.Column(db.String)
    sku_barcode = db.Column(db.String)
    sku_article = db.Column(db.String)
    sku_name = db.Column(db.String)
    sku_category = db.Column(db.String)
    sku_country = db.Column(db.String)
    sku_weight_min = db.Column(db.String)
    sku_volume_min = db.Column(db.String)
    sku_quantity_min = db.Column(db.String)
    sku_images = db.Column(db.ARRAY(db.String))
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"), nullable=False)
    subcategory = db.relationship("SubCategory", back_populates="products")
    created = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get(id):
        return Product.query.get(id)

    @staticmethod
    def create(
        price_datetime,
        price,
        price_promo,
        sku_status,
        sku_barcode,
        sku_article,
        sku_name,
        sku_category,
        sku_country,
        sku_weight_min,
        sku_volume_min,
        sku_quantity_min,
        sku_images,
        subcategory,
    ):
        product = Product(
            price_datetime=price_datetime,
            price=price,
            price_promo=price_promo,
            sku_status=sku_status,
            sku_barcode=sku_barcode,
            sku_article=sku_article,
            sku_name=sku_name,
            sku_category=sku_category,
            sku_country=sku_country,
            sku_weight_min=sku_weight_min,
            sku_volume_min=sku_volume_min,
            sku_quantity_min=sku_quantity_min,
            sku_images=sku_images,
            subcategory=subcategory,
            created=datetime.now(),
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_all_by_subcategory(subcategory):
        return Product.query.filter_by(subcategory=subcategory).all()

    @staticmethod
    def to_dict(obj):
        return {
            "id": obj.id,
            "price_datetime": obj.price_datetime,
            "price": obj.price,
            "price_promo": obj.price_promo,
            "sku_status": obj.sku_status,
            "sku_barcode": obj.sku_barcode,
            "sku_article": obj.sku_article,
            "sku_name": obj.sku_name,
            "sku_category": obj.sku_category,
            "sku_country": obj.sku_country,
            "sku_weight_min": obj.sku_weight_min,
            "sku_volume_min": obj.sku_volume_min,
            "sku_quantity_min": obj.sku_quantity_min,
            "sku_images": obj.sku_images,
            "created": obj.created,
        }
