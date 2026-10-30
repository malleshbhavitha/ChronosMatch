
import time
import statistics

from main import ChronosMatch


BUY_ORDERS = 1000
SELL_ORDERS = 1000
REPEAT_RUNS = 5


def run_benchmark():
    execution_times = []

    print("\nChronosMatch Performance Benchmark")
    print("----------------------------------")

    for run in range(1, REPEAT_RUNS + 1):
        engine = ChronosMatch()

        start_time = time.perf_counter()

        for _ in range(BUY_ORDERS):
            engine.add_order("BUY", 90, 10)

        for _ in range(SELL_ORDERS):
            engine.add_order("SELL", 110, 10)

        elapsed_time = time.perf_counter() - start_time
        execution_times.append(elapsed_time)

        print(f"Run {run}: {elapsed_time:.6f} seconds")

    average_time = statistics.mean(execution_times)
    minimum_time = min(execution_times)
    maximum_time = max(execution_times)

    total_orders = BUY_ORDERS + SELL_ORDERS
    throughput = total_orders / average_time

    print("\nBenchmark Summary")
    print("-----------------")
    print(f"BUY orders: {BUY_ORDERS}")
    print(f"SELL orders: {SELL_ORDERS}")
    print(f"Total orders: {total_orders}")
    print(f"Average time: {average_time:.6f} seconds")
    print(f"Minimum time: {minimum_time:.6f} seconds")
    print(f"Maximum time: {maximum_time:.6f} seconds")
    print(f"Average throughput: {throughput:.2f} orders/second")


if __name__ == "__main__":
    run_benchmark()
