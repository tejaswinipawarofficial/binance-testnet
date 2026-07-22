import logging
import time

logger = logging.getLogger(__name__)


class OrderManager:
    """
    Handles Binance Futures order placement
    """

    def __init__(self, client):
        self.client = client


    def create_market_order(
        self,
        symbol,
        side,
        quantity
    ):

        try:

            response = self.client.place_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

            # Wait briefly so Binance updates the order
            time.sleep(1)

            try:

                updated = self.client.get_order(
                    symbol,
                    response["orderId"]
                )

                response = updated

            except Exception:
                pass

            logger.info(response)

            return self.format_response(response)

        except Exception as e:

            logger.error(e)

            raise


    def create_limit_order(
        self,
        symbol,
        side,
        quantity,
        price
    ):

        try:

            response = self.client.place_order(

                symbol=symbol,

                side=side,

                type="LIMIT",

                quantity=quantity,

                price=price,

                timeInForce="GTC"

            )

            logger.info(response)

            return self.format_response(response)

        except Exception as e:

            logger.error(e)

            raise


    def format_response(
        self,
        response
    ):

        return {

            "orderId":
                response.get("orderId"),

            "symbol":
                response.get("symbol"),

            "side":
                response.get("side"),

            "type":
                response.get("type"),

            "status":
                response.get("status"),

            "price":
                response.get("price"),

            "avgPrice":
                response.get(
                    "avgPrice",
                    "0"
                ),

            "origQty":
                response.get(
                    "origQty"
                ),

            "executedQty":
                response.get(
                    "executedQty"
                ),

            "cumQuote":
                response.get(
                    "cumQuote"
                ),

            "timeInForce":
                response.get(
                    "timeInForce"
                ),

            "reduceOnly":
                response.get(
                    "reduceOnly"
                ),

            "closePosition":
                response.get(
                    "closePosition"
                ),

            "clientOrderId":
                response.get(
                    "clientOrderId"
                ),

            "updateTime":
                response.get(
                    "updateTime"
                ),

            "raw":
                response
        }