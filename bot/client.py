import os
import logging

from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Load local .env
load_dotenv()

logger = logging.getLogger(__name__)


class BinanceClient:
    """
    Binance Futures Testnet API Client Wrapper
    """

    def __init__(self):

        # ------------------------------------
        # Get API Keys
        # Supports:
        # 1. Local .env
        # 2. Streamlit Cloud Secrets
        # ------------------------------------

        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_SECRET_KEY")


        # Streamlit Cloud support
        if not api_key or not api_secret:

            try:
                import streamlit as st

                api_key = st.secrets.get(
                    "BINANCE_API_KEY"
                )

                api_secret = st.secrets.get(
                    "BINANCE_SECRET_KEY"
                )

            except Exception:
                pass



        if not api_key or not api_secret:

            raise Exception(
                "API Key or Secret Key missing. "
                "Add keys in .env or Streamlit Secrets."
            )



        self.client = Client(
            api_key,
            api_secret,
            testnet=True
        )


        # Binance Futures Testnet URL

        self.client.FUTURES_URL = (
            "https://testnet.binancefuture.com"
        )


        logger.info(
            "Binance Futures Testnet client initialized."
        )



    # ----------------------------------------------------
    # ACCOUNT
    # ----------------------------------------------------


    def get_balance(self):

        """
        Get USDT Futures wallet balance.
        """

        try:

            balances = (
                self.client
                .futures_account_balance()
            )


            for asset in balances:

                if asset["asset"] == "USDT":

                    return asset


            return None


        except BinanceAPIException as e:

            logger.error(
                f"Balance API Error: {e}"
            )

            raise



    def get_account_info(self):

        """
        Get Futures account information.
        """

        try:

            return self.client.futures_account()


        except BinanceAPIException as e:

            logger.error(
                f"Account Info Error: {e}"
            )

            raise



    # ----------------------------------------------------
    # MARKET DATA
    # ----------------------------------------------------


    def get_symbol_price(
        self,
        symbol="BTCUSDT"
    ):

        """
        Get latest symbol price.
        """

        try:

            return (
                self.client
                .futures_symbol_ticker(
                    symbol=symbol
                )
            )


        except BinanceAPIException as e:

            logger.error(
                f"Price API Error: {e}"
            )

            raise



    def get_exchange_info(self):

        """
        Get exchange information.
        """

        try:

            return (
                self.client
                .futures_exchange_info()
            )


        except BinanceAPIException as e:

            logger.error(e)

            raise



    # ----------------------------------------------------
    # ORDERS
    # ----------------------------------------------------


    def place_order(
        self,
        **params
    ):

        """
        Place Futures order.
        """

        try:

            response = (
                self.client
                .futures_create_order(
                    **params
                )
            )


            logger.info(
                f"Order placed successfully: {response}"
            )


            return response


        except BinanceAPIException as e:

            logger.error(
                f"Order Placement Error: {e}"
            )

            raise



    def get_order(
        self,
        symbol,
        order_id
    ):

        """
        Get order details.
        """

        try:

            return (
                self.client
                .futures_get_order(
                    symbol=symbol,
                    orderId=order_id
                )
            )


        except BinanceAPIException as e:

            logger.error(
                f"Order Fetch Error: {e}"
            )

            raise



    def cancel_order(
        self,
        symbol,
        order_id
    ):

        """
        Cancel an existing order.
        """

        try:

            return (
                self.client
                .futures_cancel_order(
                    symbol=symbol,
                    orderId=order_id
                )
            )


        except BinanceAPIException as e:

            logger.error(
                f"Cancel Order Error: {e}"
            )

            raise



    def get_open_orders(
        self,
        symbol=None
    ):

        """
        Get all open orders.
        """

        try:

            if symbol:

                return (
                    self.client
                    .futures_get_open_orders(
                        symbol=symbol
                    )
                )


            return (
                self.client
                .futures_get_open_orders()
            )


        except BinanceAPIException as e:

            logger.error(
                f"Open Orders Error: {e}"
            )

            raise