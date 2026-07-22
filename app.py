import streamlit as st

from bot.client import BinanceClient
from bot.orders import OrderManager


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Binance Futures Dashboard",
    page_icon="📈",
    layout="wide"
)


# ==============================
# CSS
# ==============================

st.markdown(
"""
<style>

.stApp{

background:#0b0e11;

}


.main-title{

font-size:45px;
font-weight:800;
text-align:center;
color:#F3BA2F;

}


.subtitle{

text-align:center;
color:#b7bdc6;
font-size:18px;

}


.card{

background:#161A1E;

padding:15px;

border-radius:15px;

border:1px solid #2b3139;

margin-bottom:10px;

}


.metric-title{

color:#b7bdc6;

font-size:14px;

}


.metric-value{

color:white;

font-size:28px;

font-weight:bold;

}


.trade-box{

background:#161A1E;

padding:20px;

border-radius:15px;

border:1px solid #2b3139;

}


.success-card{

background:#102c1c;

border-left:5px solid #00C853;

padding:15px;

border-radius:10px;

}


.error-card{

background:#321414;

border-left:5px solid red;

padding:15px;

border-radius:10px;

}


.stButton button{

width:100%;

height:50px;

font-weight:bold;

border-radius:12px;

background:#F3BA2F;

color:black;

}


footer{

visibility:hidden;

}

</style>

""",
unsafe_allow_html=True
)



# ==============================
# HEADER
# ==============================


st.markdown(
"""
<div class="main-title">

📈 Binance Futures Testnet Dashboard

</div>


<div class="subtitle">

Developed by Arshad Pinjari

</div>

""",
unsafe_allow_html=True
)


st.divider()



# ==============================
# BINANCE CONNECTION
# ==============================


try:

    client = BinanceClient()

    manager = OrderManager(client)

    api_connected = True


except Exception as e:

    api_connected = False

    st.error(e)

    st.stop()
    # ==============================
# LIVE DASHBOARD
# ==============================


balance = None
btc_price = "N/A"
eth_price = "N/A"


try:

    # Wallet Balance

    balance = client.get_balance()


    # Market Prices

    btc = client.get_symbol_price(
        "BTCUSDT"
    )

    eth = client.get_symbol_price(
        "ETHUSDT"
    )


    btc_price = float(
        btc["price"]
    )


    eth_price = float(
        eth["price"]
    )


except Exception as e:

    st.warning(
        f"Market data error: {e}"
    )



# ==============================
# DASHBOARD CARDS
# ==============================


col1, col2, col3, col4 = st.columns(4)



# Wallet

with col1:

    usdt = "0"

    if balance:

        usdt = balance.get(
            "balance",
            "0"
        )


    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    💰 Wallet Balance
    </div>

    <div class="metric-value">
    {float(usdt):,.2f}
    </div>

    <span style="color:#00FF99">
    USDT
    </span>

    </div>
    """,
    unsafe_allow_html=True
    )



# BTC

with col2:

    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    ₿ BTCUSDT
    </div>

    <div class="metric-value">
    ${btc_price:,.2f}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



# ETH

with col3:

    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    Ξ ETHUSDT
    </div>

    <div class="metric-value">
    ${eth_price:,.2f}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



# API

with col4:

    status = (
        "🟢 Connected"
        if api_connected
        else
        "🔴 Offline"
    )


    st.markdown(
    f"""
    <div class="card">

    <div class="metric-title">
    API Status
    </div>

    <div class="metric-value">
    {status}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



st.divider()
# ==============================
# TRADING PANEL
# ==============================


left, right = st.columns(
    [2, 1]
)



# ==============================
# ORDER FORM
# ==============================

with left:


    st.markdown(
    """
    <div class="trade-box">

    <h2 style="color:#F3BA2F;">
    🚀 Place New Order
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )


    symbol = st.selectbox(
        "Trading Pair",
        [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "SOLUSDT",
            "XRPUSDT",
            "DOGEUSDT"
        ]
    )


    side = st.radio(
        "Order Side",
        [
            "BUY",
            "SELL"
        ],
        horizontal=True
    )


    order_type = st.selectbox(
        "Order Type",
        [
            "MARKET",
            "LIMIT"
        ]
    )


    quantity = st.number_input(
        "Quantity",
        min_value=0.001,
        value=0.001,
        step=0.001,
        format="%.3f"
    )


    price = None


    if order_type == "LIMIT":

        try:

            ticker = client.get_symbol_price(
                symbol
            )

            current_price = float(
                ticker["price"]
            )

        except:

            current_price = 0.0


        price = st.number_input(
            "Limit Price",
            min_value=0.0,
            value=current_price,
            step=1.0
        )


    st.write("")


    place_order = st.button(
        "🚀 PLACE ORDER"
    )





# ==============================
# ORDER SUMMARY
# ==============================


with right:


    st.markdown(
    """
    <div class="trade-box">

    <h2 style="
    color:#F3BA2F;
    margin-bottom:25px;
    ">
    📋 Order Summary
    </h2>

    </div>
    """,
    unsafe_allow_html=True
    )

    st.write("")

    summary = {

        "💹 Pair": symbol,

        "📈 Side": side,

        "📄 Type": order_type,

        "📦 Quantity": quantity

    }



    if order_type == "LIMIT":

        summary["💲 Price"] = price

    else:

        summary["⚡ Execution"] = "Market Price"



    for key, value in summary.items():

        st.markdown(
        f"""
        <div class="card">

        <div class="metric-title">

        {key}

        </div>


        <div style="
        color:#00FF99;
        font-size:20px;
        font-weight:bold;
        ">

        {value}

        </div>


        </div>
        """,
        unsafe_allow_html=True
        )


st.divider()
# ==============================
# ORDER EXECUTION
# ==============================


if place_order:


    progress = st.progress(0)

    message = st.empty()


    try:


        message.info(
            "🔄 Connecting to Binance..."
        )

        progress.progress(25)



        message.info(
            "✅ Validating order..."
        )

        progress.progress(50)



        message.info(
            "📤 Sending order..."
        )

        progress.progress(75)



        # --------------------------
        # MARKET ORDER
        # --------------------------

        if order_type == "MARKET":


            response = manager.create_market_order(

                symbol=symbol,

                side=side,

                quantity=quantity

            )


        # --------------------------
        # LIMIT ORDER
        # --------------------------

        else:


            response = manager.create_limit_order(

                symbol=symbol,

                side=side,

                quantity=quantity,

                price=price

            )



        progress.progress(100)


        message.success(
            "🎉 Order Placed Successfully!"
        )


        st.balloons()


        st.write("")



        st.markdown(
        """
        <div class="success-card">

        <h2 style="color:#00C853;">

        ✅ Order Details

        </h2>

        </div>
        """,
        unsafe_allow_html=True
        )



        c1, c2, c3 = st.columns(3)



        with c1:


            st.metric(
                "🆔 Order ID",
                response.get(
                    "orderId",
                    "N/A"
                )
            )


            st.metric(
                "💹 Symbol",
                response.get(
                    "symbol",
                    "N/A"
                )
            )


            st.metric(
                "📈 Side",
                response.get(
                    "side",
                    "N/A"
                )
            )



        with c2:


            st.metric(
                "📄 Type",
                response.get(
                    "type",
                    "N/A"
                )
            )


            st.metric(
                "📌 Status",
                response.get(
                    "status",
                    "N/A"
                )
            )


            st.metric(
                "📦 Executed Qty",
                response.get(
                    "executedQty",
                    "0"
                )
            )



        with c3:


            st.metric(
                "💲 Avg Price",
                response.get(
                    "avgPrice",
                    "N/A"
                )
            )


            st.metric(
                "🔑 Client ID",
                response.get(
                    "clientOrderId",
                    "N/A"
                )
            )



        st.download_button(

            "📥 Download Order Receipt",

            data=str(response),

            file_name="order_receipt.txt"

        )



        with st.expander(
            "View Raw Response"
        ):

            st.json(response)



    except Exception as e:


        progress.empty()

        message.empty()


        st.markdown(
        """
        <div class="error-card">

        <h3 style="color:red">

        ❌ Order Failed

        </h3>

        </div>
        """,
        unsafe_allow_html=True
        )


        st.error(
            str(e)
        )
        # ==============================
# SIDEBAR
# ==============================


with st.sidebar:


    st.title(
        "📈 Binance Dashboard"
    )


    st.success(
        "🟢 Testnet Connected"
    )


    st.divider()


    st.subheader(
        "📊 Quick Stats"
    )


    if balance:

        st.metric(
            "💰 Wallet",
            f"{float(balance['balance']):,.2f} USDT"
        )


    st.metric(
        "₿ BTC",
        f"${btc_price:,.2f}"
        if btc_price != "N/A"
        else "N/A"
    )


    st.metric(
        "Ξ ETH",
        f"${eth_price:,.2f}"
        if eth_price != "N/A"
        else "N/A"
    )


    st.divider()


    st.subheader(
        "💡 Trading Tips"
    )


    st.info(
        """
• Verify symbol before trading.

• MARKET executes instantly.

• LIMIT waits for your price.

• This uses Binance Futures Testnet.

• Never share API keys.
"""
    )


    if st.button(
        "🔄 Refresh Dashboard"
    ):

        st.rerun()



# ==============================
# TRADINGVIEW CHART
# ==============================


st.divider()


st.subheader(
    "📈 Live Market Chart"
)


chart_symbol = symbol.replace(
    "USDT",
    "USD"
)


tradingview = f"""

<div>

<script src="
https://s3.tradingview.com/tv.js">
</script>


<script>

new TradingView.widget({{

"width":"100%",

"height":500,

"symbol":"BINANCE:{chart_symbol}",

"interval":"15",

"timezone":"Etc/UTC",

"theme":"dark",

"style":"1",

"locale":"en",

"enable_publishing":false,

"allow_symbol_change":true,

"container_id":"chart"

}});


</script>


<div id="chart"></div>


</div>

"""


st.components.v1.html(
    tradingview,
    height=520
)



# ==============================
# FOOTER
# ==============================


st.divider()


st.markdown(
"""
<div style="
text-align:center;
color:#9aa4af;
padding:20px;
">


<h3 style="color:#F3BA2F">

Thanks to Use our Portal

</h3>
<br>
Copyright © 2026. All Rights Reserved ❤️ HandCrafted by Arshad_Pinjari


</div>

""",
unsafe_allow_html=True
)