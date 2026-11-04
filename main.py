


import math


class ChronosMatch:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trade_history = []
        self.next_order_id = 1

    def add_order(self, order_type, price, quantity):
        if not isinstance(order_type, str):
            raise ValueError("Order type must be BUY or SELL")

        order_type = order_type.strip().upper()

        if order_type not in ("BUY", "SELL"):
            raise ValueError("Order type must be BUY or SELL")

        if (
            not isinstance(price, (int, float))
            or isinstance(price, bool)
            or not math.isfinite(price)
        ):
            raise ValueError("Price must be a finite number")

        if price <= 0:
            raise ValueError("Price must be positive")

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        order = {
            "order_id": self.next_order_id,
            "price": price,
            "quantity": quantity,
        }

        self.next_order_id += 1

        if order_type == "BUY":
            self.match_buy(order, quantity)
        else:
            self.match_sell(order, quantity)

        return order["order_id"]

    def record_trade(self, order_type, price, quantity):
        self.trade_history.append({
            "incoming_order": order_type,
            "price": price,
            "quantity": quantity,
        })

        print(f"Trade executed: {quantity} units at {price}")

    def match_buy(self, order, quantity):
        price = order["price"]

        # Lowest SELL price first; earliest order first at equal prices.
        self.sell_orders.sort(
            key=lambda item: (item["price"], item["order_id"])
        )

        while self.sell_orders and quantity > 0:
            sell = self.sell_orders[0]

            if price < sell["price"]:
                break

            traded = min(quantity, sell["quantity"])

            self.record_trade("BUY", sell["price"], traded)

            quantity -= traded
            sell["quantity"] -= traded

            if sell["quantity"] == 0:
                self.sell_orders.pop(0)

        if quantity > 0:
            self.buy_orders.append({
                "order_id": order["order_id"],
                "price": price,
                "quantity": quantity,
            })

        # Highest BUY price first; earliest order first at equal prices.
        self.buy_orders.sort(
            key=lambda item: (-item["price"], item["order_id"])
        )

    def match_sell(self, order, quantity):
        price = order["price"]

        # Highest BUY price first; earliest order first at equal prices.
        self.buy_orders.sort(
            key=lambda item: (-item["price"], item["order_id"])
        )

        while self.buy_orders and quantity > 0:
            buy = self.buy_orders[0]

            if price > buy["price"]:
                break

            traded = min(quantity, buy["quantity"])

            self.record_trade("SELL", buy["price"], traded)

            quantity -= traded
            buy["quantity"] -= traded

            if buy["quantity"] == 0:
                self.buy_orders.pop(0)

        if quantity > 0:
            self.sell_orders.append({
                "order_id": order["order_id"],
                "price": price,
                "quantity": quantity,
            })

        # Lowest SELL price first; earliest order first at equal prices.
        self.sell_orders.sort(
            key=lambda item: (item["price"], item["order_id"])
        )

    def cancel_order(self, order_id):
        if not isinstance(order_id, int) or isinstance(order_id, bool):
            raise ValueError("Order ID must be an integer")

        for orders in (self.buy_orders, self.sell_orders):
            for index, order in enumerate(orders):
                if order["order_id"] == order_id:
                    orders.pop(index)
                    print(f"Order {order_id} cancelled.")
                    return True

        print(f"Order {order_id} not found.")
        return False

    # Day 9: Order Book Summary
    def get_order_book_summary(self):
        best_buy = (
            self.buy_orders[0]["price"]
            if self.buy_orders else None
        )

        best_sell = (
            self.sell_orders[0]["price"]
            if self.sell_orders else None
        )

        spread = (
            best_sell - best_buy
            if best_buy is not None and best_sell is not None
            else None
        )

        return {
            "total_buy_orders": len(self.buy_orders),
            "total_sell_orders": len(self.sell_orders),
            "best_buy_price": best_buy,
            "best_sell_price": best_sell,
            "bid_ask_spread": spread,
        }

    def show_order_book(self):
        print("\n" + "=" * 55)
        print("              CHRONOSMATCH ORDER BOOK")
        print("=" * 55)

        for title, orders in (
            ("BUY ORDERS", self.buy_orders),
            ("SELL ORDERS", self.sell_orders),
        ):
            print(f"\n{title}")
            print("-" * 55)
            print(f"{'ORDER ID':<12}{'PRICE':<18}{'QUANTITY':<12}")

            if not orders:
                print("No pending orders.")
                continue

            for order in orders:
                print(
                    f"{order['order_id']:<12}"
                    f"{order['price']:<18}"
                    f"{order['quantity']:<12}"
                )

        summary = self.get_order_book_summary()

        print("\nORDER BOOK SUMMARY")
        print("-" * 55)
        print("Total BUY orders:", summary["total_buy_orders"])
        print("Total SELL orders:", summary["total_sell_orders"])
        print("Best BUY price:", summary["best_buy_price"])
        print("Best SELL price:", summary["best_sell_price"])

        if summary["bid_ask_spread"] is not None:
            print("Bid-Ask Spread:", summary["bid_ask_spread"])
        else:
            print("Bid-Ask Spread: Not available")

        print("\n" + "=" * 55)

    # Day 10: Trade History Summary
    def get_trade_summary(self):
        total_trades = len(self.trade_history)

        total_quantity = sum(
            trade["quantity"]
            for trade in self.trade_history
        )

        total_value = sum(
            trade["price"] * trade["quantity"]
            for trade in self.trade_history
        )

        average_price = (
            total_value / total_quantity
            if total_quantity > 0
            else None
        )

        return {
            "total_trades": total_trades,
            "total_quantity": total_quantity,
            "average_trade_price": average_price,
        }

    def show_trade_history(self):
        print("\n" + "=" * 55)
        print("             CHRONOSMATCH TRADE HISTORY")
        print("=" * 55)

        if not self.trade_history:
            print("No trades executed yet.")
        else:
            print(
                f"{'NO.':<8}{'ORDER TYPE':<15}"
                f"{'PRICE':<15}{'QUANTITY':<12}"
            )

            print("-" * 55)

            for number, trade in enumerate(
                self.trade_history, start=1
            ):
                print(
                    f"{number:<8}"
                    f"{trade['incoming_order']:<15}"
                    f"{trade['price']:<15}"
                    f"{trade['quantity']:<12}"
                )

        summary = self.get_trade_summary()

        print("\nTRADE SUMMARY")
        print("-" * 55)
        print("Total trades:", summary["total_trades"])
        print("Total traded quantity:", summary["total_quantity"])

        if summary["average_trade_price"] is not None:
            print(
                "Average trade price:",
                round(summary["average_trade_price"], 2)
            )
        else:
            print("Average trade price: Not available")

        print("=" * 55)


if __name__ == "__main__":
    engine = ChronosMatch()

    engine.add_order("BUY", 100, 10)
    engine.add_order("BUY", 95, 5)
    engine.add_order("SELL", 110, 3)
    engine.add_order("SELL", 100, 4)

    engine.show_order_book()
    engine.show_trade_history()
