
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
        self.sell_orders.sort(key=lambda item: item["price"])

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

        self.buy_orders.sort(
            key=lambda item: item["price"],
            reverse=True,
        )

    def match_sell(self, order, quantity):
        price = order["price"]
        self.buy_orders.sort(
            key=lambda item: item["price"],
            reverse=True,
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

        self.sell_orders.sort(key=lambda item: item["price"])

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

    def show_order_book(self):
        print("\n" + "=" * 45)
        print("          CHRONOSMATCH ORDER BOOK")
        print("=" * 45)

        for title, orders in (
            ("BUY ORDERS", self.buy_orders),
            ("SELL ORDERS", self.sell_orders),
        ):
            print(f"\n{title}")
            print("-" * 45)
            print(f"{'ORDER ID':<12}{'PRICE':<15}{'QUANTITY':<12}")

            if not orders:
                print("No pending orders.")
                continue

            for order in orders:
                print(
                    f"{order['order_id']:<12}"
                    f"{order['price']:<15}"
                    f"{order['quantity']:<12}"
                )

        print("\n" + "=" * 45)

    def show_trade_history(self):
        print("\nCHRONOSMATCH TRADE HISTORY")
        print("-" * 45)

        if not self.trade_history:
            print("No trades executed yet.")
            return

        for number, trade in enumerate(self.trade_history, start=1):
            print(
                f"{number}. Incoming order: {trade['incoming_order']}, "
                f"Price: {trade['price']}, "
                f"Quantity: {trade['quantity']}"
            )


if __name__ == "__main__":
    engine = ChronosMatch()

    engine.add_order("BUY", 100, 10)
    engine.add_order("BUY", 95, 5)
    engine.add_order("SELL", 110, 3)
    engine.add_order("SELL", 100, 4)

    engine.show_order_book()
    engine.show_trade_history()
