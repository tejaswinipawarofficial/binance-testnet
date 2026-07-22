import argparse
import logging

from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_limit_order
)

from bot.logging_config import setup_logging


def main():

    setup_logging()

    logger = logging.getLogger(__name__)


    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )


    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading symbol e.g BTCUSDT"
    )

    parser.add_argument(
        "--side",
        required=True,
        help="BUY or SELL"
    )

    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT"
    )

    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity"
    )

    parser.add_argument(
        "--price",
        required=False,
        help="Required for LIMIT orders"
    )


    args = parser.parse_args()


    try:

        side = validate_side(args.side)

        order_type = validate_order_type(
            args.order_type
        )

        quantity = validate_quantity(
            args.quantity
        )

        price = None

        if args.price:
            price = validate_price(
                args.price
            )


        validate_limit_order(
            order_type,
            price
        )


        client = BinanceClient()

        manager = OrderManager(client)


        print("\nOrder Summary")
        print("----------------")
        print(
            "Symbol:",
            args.symbol
        )
        print(
            "Side:",
            side
        )
        print(
            "Type:",
            order_type
        )
        print(
            "Quantity:",
            quantity
        )


        if order_type == "MARKET":

            result = manager.create_market_order(
                args.symbol,
                side,
                quantity
            )

        else:

            result = manager.create_limit_order(
                args.symbol,
                side,
                quantity,
                price
            )


        print("\nOrder Response")
        print("----------------")
        print(result)

        print(
            "\nOrder placed successfully!"
        )


    except Exception as e:

        logger.error(e)

        print(
            "Order failed:",
            e
        )


if __name__ == "__main__":
    main()