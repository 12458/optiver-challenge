# Setup
import time
from optibook.synchronous_client import Exchange

import logging

logger = logging.getLogger("client")
logger.setLevel("ERROR")
instrument_id_a = "PHILIPS_A"
instrument_id_b = "PHILIPS_B"
print("Setup was successful.")


def get_bid_ask_mid(instrument_id, mode):
    stock_order_book = e.get_last_price_book(instrument_id)
    # Obtain best bid and ask prices from order book
    if mode == "bid":
        while True:
            try:
                return stock_order_book.bids[0].price
            except:
                stock_order_book = e.get_last_price_book(instrument_id)
    else:
        while True:
            try:
                return stock_order_book.asks[0].price
            except:
                stock_order_book = e.get_last_price_book(instrument_id)


e = Exchange()
a = e.connect()
# Get out of all positions you are currently holding, regarless of the loss involved. That means selling whatever
# you are long, and buying-back whatever you are short. Be sure you know what you are doing when you use this logic.
print(e.get_positions())
for s, p in e.get_positions().items():
    if p > 0:
        e.insert_order(s, price=1, volume=p, side="ask", order_type="ioc")
    elif p < 0:
        e.insert_order(s, price=100000, volume=-p, side="bid", order_type="ioc")
print(e.get_positions())

while True:
    try:
        while True:
            trig = False
            bef = e.get_pnl()
            if get_bid_ask_mid(instrument_id_a, "ask") < get_bid_ask_mid(
                instrument_id_b, "bid"
            ):
                # buy a, sell b
                e.insert_order(
                    instrument_id_a,
                    price=10000,
                    volume=10,
                    side="bid",
                    order_type="limit",
                )
                e.insert_order(
                    instrument_id_b, price=1, volume=10, side="ask", order_type="limit"
                )
                print(
                    f"Buy A, Sell B @ ASK A: {get_bid_ask_mid(instrument_id_a, 'ask'):.2f} | BID B: {get_bid_ask_mid(instrument_id_b, 'bid'):.2f} | EXPECTED PROFIT: {get_bid_ask_mid(instrument_id_b, 'bid') - get_bid_ask_mid(instrument_id_a, 'ask'):.2f}"
                )
                trig = True
            aft = e.get_pnl()
            if trig:
                print(f"POSITIONS: {e.get_positions()} | PROFIT: {aft - bef:.2f}")
            trig = False
            bef = e.get_pnl()
            if get_bid_ask_mid(instrument_id_b, "ask") < get_bid_ask_mid(
                instrument_id_a, "bid"
            ):
                # buy b, sell a
                e.insert_order(
                    instrument_id_b,
                    price=10000,
                    volume=10,
                    side="bid",
                    order_type="limit",
                )
                e.insert_order(
                    instrument_id_a, price=1, volume=10, side="ask", order_type="limit"
                )
                print(
                    f"Buy B, Sell A @ ASK B: {get_bid_ask_mid(instrument_id_b, 'ask'):.2f} | BID A: {get_bid_ask_mid(instrument_id_a, 'bid'):.2f} | EXPECTED PROFIT: {get_bid_ask_mid(instrument_id_a, 'bid') - get_bid_ask_mid(instrument_id_b, 'ask'):.2f}"
                )
                trig = True
            aft = e.get_pnl()
            if trig:
                print(f"POSITIONS: {e.get_positions()} | PROFIT: {aft - bef:.2f}")
            time.sleep(0.5)
    except:
        e = Exchange()
        a = e.connect()
        # Get out of all positions you are currently holding, regarless of the loss involved. That means selling whatever
        # you are long, and buying-back whatever you are short. Be sure you know what you are doing when you use this logic.
        print(e.get_positions())
        for s, p in e.get_positions().items():
            if p > 0:
                e.insert_order(s, price=1, volume=p, side="ask", order_type="ioc")
            elif p < 0:
                e.insert_order(s, price=100000, volume=-p, side="bid", order_type="ioc")
        print(e.get_positions())
