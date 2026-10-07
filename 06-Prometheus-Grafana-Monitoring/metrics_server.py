from prometheus_client import start_http_server, Counter, Gauge, Summary
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Metrics definitions
order_dispatches_total = Counter("order_dispatches_total", "Cumulative count of orders dispatched")
current_pending_orders = Gauge("current_pending_orders", "Current queue size of pending orders")
active_riders_count = Gauge("active_riders_count", "Number of riders currently on delivery routes")
delivery_duration_seconds = Summary("delivery_duration_seconds", "Trip duration in seconds per completed order")

def generate_telemetry():
    # Simulate delivery logistics numbers
    pending = random.randint(12, 25)      # Exceeds alert threshold of 12 for alerts
    in_transit = random.randint(8, 22)
    new_dispatches = random.randint(2, 6)
    trip_time = random.uniform(18.0, 48.0)

    order_dispatches_total.inc(new_dispatches)
    current_pending_orders.set(pending)
    active_riders_count.set(in_transit)
    delivery_duration_seconds.observe(trip_time)

    logging.info(f"Telemetry -> Dispatched: +{new_dispatches} | Pending: {pending} | In-Transit: {in_transit} | Avg Duration: {trip_time:.2f}s")

if __name__ == "__main__":
    PORT = 8000
    logging.info(f"Starting Prometheus Metrics Exporter on port {PORT}...")
    start_http_server(PORT, addr="0.0.0.0")
    logging.info("Metrics exporter online. Emitting live operational telemetry...")

    while True:
        generate_telemetry()
        time.sleep(1)
