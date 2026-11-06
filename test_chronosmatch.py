

import unittest
from io import StringIO
from contextlib import redirect_stdout

from main import ChronosMatch


class TestChronosMatch(unittest.TestCase):

    def setUp(self):
        self.engine = ChronosMatch()

    def test_add_buy_order(self):
        order_id = self.engine.add_order("BUY", 100, 10)

        self.assertEqual(order_id, 1)
        self.assertEqual(len(self.engine.buy_orders), 1)

    def test_add_sell_order(self):
        order_id = self.engine.add_order("SELL", 110, 5)

        self.assertEqual(order_id, 1)
        self.assertEqual(len(self.engine.sell_orders), 1)

    def test_order_type_is_case_insensitive(self):
        self.engine.add_order(" buy ", 100, 5)

        self.assertEqual(len(self.engine.buy_orders), 1)

    def test_invalid_order_type(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("HOLD", 100, 5)

    def test_non_string_order_type(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(123, 100, 5)


    def test_zero_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", 0, 5)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", -10, 5)

    def test_infinite_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", float("inf"), 5)

    def test_nan_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", float("nan"), 5)

    def test_boolean_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", True, 5)

    def test_invalid_price_type(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", "100", 5)



    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", 100, 0)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", 100, -5)

    def test_float_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", 100, 2.5)

    def test_boolean_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_order("BUY", 100, True)

    

    def test_matching_orders(self):
        self.engine.add_order("SELL", 100, 5)
        self.engine.add_order("BUY", 100, 5)

        self.assertEqual(len(self.engine.trade_history), 1)
        self.assertEqual(
            self.engine.trade_history[0]["quantity"], 5
        )
        self.assertEqual(len(self.engine.sell_orders), 0)
        self.assertEqual(len(self.engine.buy_orders), 0)

    def test_partial_matching(self):
        self.engine.add_order("SELL", 100, 5)
        self.engine.add_order("BUY", 100, 3)

        self.assertEqual(len(self.engine.trade_history), 1)
        self.assertEqual(
            self.engine.sell_orders[0]["quantity"], 2
        )

    def test_no_matching_when_prices_do_not_cross(self):
        self.engine.add_order("SELL", 110, 5)
        self.engine.add_order("BUY", 100, 5)

        self.assertEqual(len(self.engine.trade_history), 0)
        self.assertEqual(len(self.engine.buy_orders), 1)
        self.assertEqual(len(self.engine.sell_orders), 1)

    def test_trade_executes_at_resting_sell_price(self):
        self.engine.add_order("SELL", 100, 5)
        self.engine.add_order("BUY", 110, 5)

        self.assertEqual(
            self.engine.trade_history[0]["price"], 100
        )

    def test_trade_executes_at_resting_buy_price(self):
        self.engine.add_order("BUY", 110, 5)
        self.engine.add_order("SELL", 100, 5)

        self.assertEqual(
            self.engine.trade_history[0]["price"], 110
        )

  

    def test_buy_uses_lowest_sell_price_first(self):
        self.engine.add_order("SELL", 105, 5)
        self.engine.add_order("SELL", 100, 5)
        self.engine.add_order("BUY", 110, 5)

        self.assertEqual(
            self.engine.trade_history[0]["price"], 100
        )

    def test_sell_uses_highest_buy_price_first(self):
        self.engine.add_order("BUY", 100, 5)
        self.engine.add_order("BUY", 105, 5)
        self.engine.add_order("SELL", 95, 5)

        self.assertEqual(
            self.engine.trade_history[0]["price"], 105
        )


    def test_buy_orders_follow_fifo_priority(self):
        first_id = self.engine.add_order("BUY", 100, 5)
        second_id = self.engine.add_order("BUY", 100, 5)

        self.engine.add_order("SELL", 100, 5)

        self.assertEqual(
            self.engine.trade_history[0]["quantity"], 5
        )
        self.assertEqual(
            [order["order_id"] for order in self.engine.buy_orders],
            [second_id]
        )
        self.assertNotEqual(first_id, second_id)

    def test_sell_orders_follow_fifo_priority(self):
        first_id = self.engine.add_order("SELL", 100, 5)
        second_id = self.engine.add_order("SELL", 100, 5)

        self.engine.add_order("BUY", 100, 5)

        self.assertEqual(
            [order["order_id"] for order in self.engine.sell_orders],
            [second_id]
        )
        self.assertNotEqual(first_id, second_id)

  

    def test_cancel_buy_order(self):
        order_id = self.engine.add_order("BUY", 100, 5)

        result = self.engine.cancel_order(order_id)

        self.assertTrue(result)
        self.assertEqual(len(self.engine.buy_orders), 0)

    def test_cancel_sell_order(self):
        order_id = self.engine.add_order("SELL", 110, 5)

        result = self.engine.cancel_order(order_id)

        self.assertTrue(result)
        self.assertEqual(len(self.engine.sell_orders), 0)

    def test_cancel_nonexistent_order(self):
        result = self.engine.cancel_order(999)

        self.assertFalse(result)

    def test_cancel_invalid_order_id(self):
        with self.assertRaises(ValueError):
            self.engine.cancel_order("abc")


    def test_order_book_summary(self):
        self.engine.add_order("BUY", 100, 5)
        self.engine.add_order("SELL", 110, 5)

        summary = self.engine.get_order_book_summary()

        self.assertEqual(summary["total_buy_orders"], 1)
        self.assertEqual(summary["total_sell_orders"], 1)
        self.assertEqual(summary["best_buy_price"], 100)
        self.assertEqual(summary["best_sell_price"], 110)
        self.assertEqual(summary["bid_ask_spread"], 10)

    def test_empty_order_book_summary(self):
        summary = self.engine.get_order_book_summary()

        self.assertIsNone(summary["best_buy_price"])
        self.assertIsNone(summary["best_sell_price"])
        self.assertIsNone(summary["bid_ask_spread"])


    def test_trade_summary(self):
        self.engine.add_order("SELL", 100, 5)
        self.engine.add_order("BUY", 100, 5)

        summary = self.engine.get_trade_summary()

        self.assertEqual(summary["total_trades"], 1)
        self.assertEqual(summary["total_quantity"], 5)
        self.assertEqual(summary["average_trade_price"], 100)

    def test_empty_trade_summary(self):
        summary = self.engine.get_trade_summary()

        self.assertEqual(summary["total_trades"], 0)
        self.assertEqual(summary["total_quantity"], 0)
        self.assertIsNone(summary["average_trade_price"])

    

    def test_order_book_display(self):
        output = StringIO()

        with redirect_stdout(output):
            self.engine.show_order_book()

        self.assertIn("CHRONOSMATCH ORDER BOOK", output.getvalue())

    def test_trade_history_display(self):
        output = StringIO()

        with redirect_stdout(output):
            self.engine.show_trade_history()

        self.assertIn("CHRONOSMATCH TRADE HISTORY", output.getvalue())


if __name__ == "__main__":
    unittest.main()
