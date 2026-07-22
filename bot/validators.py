import logging

logger = logging.getLogger(__name__)


VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]


def validate_side(side):
    side = side.upper()

    if side not in VALID_SIDES:
        raise ValueError(
            "Invalid side. Use BUY or SELL"
        )

    return side


def validate_order_type(order_type):
    order_type = order_type.upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            "Invalid order type. Use MARKET or LIMIT"
        )

    return order_type


def validate_quantity(quantity):

    try:
        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError

        return quantity

    except:
        raise ValueError(
            "Quantity must be a positive number"
        )


def validate_price(price):

    try:
        price = float(price)

        if price <= 0:
            raise ValueError

        return price

    except:
        raise ValueError(
            "Price must be a positive number"
        )


def validate_limit_order(order_type, price):

    if order_type == "LIMIT" and price is None:
        raise ValueError(
            "Price is required for LIMIT order"
        )