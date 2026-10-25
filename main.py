
class ChronosMatch:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order_type, price, quantity):
        if order_type == "BUY":
            for sell in self.sell_orders:
                if price >= sell["price"] and quantity > 0:
                    traded = min(quantity, sell["quantity"])
                    print(f"Trade executed: {traded} units at {sell['price']}")
                    quantity -= traded
                    sell["quantity"] -= traded

            self.sell_orders = [
                order for order in self.sell_orders
                if order["quantity"] > 0
            ]

            if quantity > 0:
                self.buy_orders.append({
                    "price": price,
                    "quantity": quantity
                })

        elif order_type == "SELL":
            for buy in self.buy_orders:
                if price <= buy["price"] and quantity > 0:
                    traded = min(quantity, buy["quantity"])
                    print(f"Trade executed: {traded} units at {buy['price']}")
                    quantity -= traded
                    buy["quantity"] -= traded

            self.buy_orders = [
                order for order in self.buy_orders
                if order["quantity"] > 0
            ]

            if quantity > 0:
                self.sell_orders.append({
                    "price": price,
                    "quantity": quantity
                })


engine = ChronosMatch()

engine.add_order("BUY", 100, 10)
engine.add_order("SELL", 95, 5)
engine.add_order("SELL", 100, 3)

print("Remaining BUY orders:", engine.buy_orders)
print("Remaining SELL orders:", engine.sell_orders)
