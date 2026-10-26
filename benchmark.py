import time
from main import ChronosMatch


def run_benchmark(number_of_orders=1000):
    engine = ChronosMatch()

    start_time = time.perf_counter()

    # Add BUY orders that will remain in the order book
    for _ in range(number_of_orders):
        engine.add_order("BUY", 90, 1)

    # Add SELL orders that will remain in the order book
    for _ in range(number_of_orders):
        engine.add_order("SELL", 110, 1)

    end_time = time.perf_counter()

    elapsed = end_time - start_time
    total_orders = number_of_orders * 2

    print("\nChronosMatch Performance Benchmark")
    print("---------------------------------")
    print(f"BUY orders: {number_of_orders}")
    print(f"SELL orders: {number_of_orders}")
    print(f"Total orders processed: {total_orders}")
    print(f"Elapsed time: {elapsed:.6f} seconds")

    if elapsed > 0:
        print(f"Throughput: {total_orders / elapsed:.2f} orders/second")


if __name__ == "__main__":
    run_benchmark()
