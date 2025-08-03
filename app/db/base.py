from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.db.models import (
    user,
    product_category,
    product,
    order,
    order_item,
    payment,
    address,
    product_review
)