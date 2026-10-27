
import unittest
from io import StringIO
from contextlib import redirect_stdout

from main import ChronosMatch


class TestChronosMatch(unittest.TestCase):

    def test_matching_orders(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 10)
        engine.add_order("SELL", 95, 5)

        self.assertEqual(
            engine.buy_orders,
            [{"order_id": 1, "price": 100, "quantity": 5}]
        )
        self.assertEqual(engine.sell_orders, [])

    def test_partial_matching(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 3)
        engine.add_order("SELL", 90, 5)

        self.assertEqual(engine.buy_orders, [])
        self.assertEqual(
            engine.sell_orders,
            [{"order_id": 2, "price": 90, "quantity": 2}]
        )

    def test_price_priority(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 95, 2)
        engine.add_order("BUY", 100, 3)

        self.assertEqual(
            [order["price"] for order in engine.buy_orders],
            [100, 95]
        )

    def test_invalid_quantity(self):
        engine = ChronosMatch()

        with self.assertRaises(ValueError):
            engine.add_order("BUY", 100, 0)

    def test_invalid_price(self):
        engine = ChronosMatch()

        with self.assertRaises(ValueError):
            engine.add_order("BUY", -100, 2)

    def test_invalid_order_type(self):
        engine = ChronosMatch()

        with self.assertRaises(ValueError):
            engine.add_order("HOLD", 100, 1)

    def test_trade_history(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 10)
        engine.add_order("SELL", 95, 5)

        self.assertEqual(len(engine.trade_history), 1)
        self.assertEqual(engine.trade_history[0]["price"], 100)
        self.assertEqual(engine.trade_history[0]["quantity"], 5)

    def test_cancel_order(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 10)
        order_id = engine.add_order("BUY", 90, 5)

        self.assertTrue(engine.cancel_order(order_id))
        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(engine.buy_orders[0]["price"], 100)

    def test_cancel_nonexistent_order(self):
        engine = ChronosMatch()

        self.assertFalse(engine.cancel_order(999))

    def test_unique_order_ids(self):
        engine = ChronosMatch()
        first_id = engine.add_order("BUY", 100, 10)
        second_id = engine.add_order("BUY", 90, 5)

        self.assertNotEqual(first_id, second_id)

    def test_cancel_only_selected_order(self):
        engine = ChronosMatch()
        first_id = engine.add_order("BUY", 100, 10)
        second_id = engine.add_order("BUY", 100, 5)

        engine.cancel_order(second_id)

        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(
            engine.buy_orders[0]["order_id"], first_id
        )

    def test_order_book_display(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 10)
        engine.add_order("SELL", 110, 5)

        output = StringIO()

        with redirect_stdout(output):
            engine.show_order_book()

        result = output.getvalue()

        self.assertIn("BUY ORDERS", result)
        self.assertIn("SELL ORDERS", result)
        self.assertIn("ORDER ID", result)
        self.assertIn("100", result)
        self.assertIn("110", result)
        self.assertIn("QUANTITY", result)

    def test_empty_order_book_display(self):
        engine = ChronosMatch()
        output = StringIO()

        with redirect_stdout(output):
            engine.show_order_book()

        self.assertIn("No pending orders.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
