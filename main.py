
class ChronosMatch:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order_type, price, quantity):
        order_type = order_type.strip().upper()

        if order_type not in ("BUY", "SELL"):
            raise ValueError("Order type must be BUY or SELL")

        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive")

        if order_type == "BUY":
            self.match_buy(price, quantity)
        else:
            self.match_sell(price, quantity)

    def match_buy(self, price, quantity):
        # Lowest sell price gets priority
        self.sell_orders.sort(key=lambda order: order["price"])

        while self.sell_orders and quantity > 0:
            sell = self.sell_orders[0]

            if price < sell["price"]:
                break

            traded = min(quantity, sell["quantity"])

            print(
                f"Trade executed: {traded} units "
                f"at {sell['price']}"
            )

            quantity -= traded
            sell["quantity"] -= traded

            if sell["quantity"] == 0:
                self.sell_orders.pop(0)

        if quantity > 0:
            self.buy_orders.append({
                "price": price,
                "quantity": quantity
            })

        # Highest buy price gets priority
        self.buy_orders.sort(
            key=lambda order: order["price"],
            reverse=True
        )

    def match_sell(self, price, quantity):
        # Highest buy price gets priority
        self.buy_orders.sort(
            key=lambda order: order["price"],
            reverse=True
        )

        while self.buy_orders and quantity > 0:
            buy = self.buy_orders[0]

            if price > buy["price"]:
                break

            traded = min(quantity, buy["quantity"])

            print(
                f"Trade executed: {traded} units "
                f"at {buy['price']}"
            )

            quantity -= traded
            buy["quantity"] -= traded

            if buy["quantity"] == 0:
                self.buy_orders.pop(0)

        if quantity > 0:
            self.sell_orders.append({
                "price": price,
                "quantity": quantity
            })

        # Lowest sell price gets priority
        self.sell_orders.sort(key=lambda order: order["price"])

    def show_order_book(self):
        print("\nRemaining BUY orders:", self.buy_orders)
        print("Remaining SELL orders:", self.sell_orders)


if __name__ == "__main__":
    engine = ChronosMatch()

    engine.add_order("BUY", 100, 10)
    engine.add_order("SELL", 95, 5)
    engine.add_order("SELL", 100, 3)

    engine.show_order_book()

