
import unittest
from main import ChronosMatch


class TestChronosMatch(unittest.TestCase):

    def test_matching_orders(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 10)
        engine.add_order("SELL", 95, 5)

        self.assertEqual(
            engine.buy_orders,
            [{"price": 100, "quantity": 5}]
        )
        self.assertEqual(engine.sell_orders, [])

    def test_partial_matching(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 100, 3)
        engine.add_order("SELL", 90, 5)

        self.assertEqual(engine.buy_orders, [])
        self.assertEqual(
            engine.sell_orders,
            [{"price": 90, "quantity": 2}]
        )

    def test_price_priority(self):
        engine = ChronosMatch()
        engine.add_order("BUY", 95, 2)
        engine.add_order("BUY", 100, 3)

        self.assertEqual(
            engine.buy_orders,
            [
                {"price": 100, "quantity": 3},
                {"price": 95, "quantity": 2}
            ]
        )

    def test_invalid_quantity(self):
        engine = ChronosMatch()

        with self.assertRaises(ValueError):
            engine.add_order("BUY", 100, 0)

    def test_invalid_order_type(self):
        engine = ChronosMatch()

        with self.assertRaises(ValueError):
            engine.add_order("HOLD", 100, 1)


if __name__ == "__main__":
    unittest.main()
