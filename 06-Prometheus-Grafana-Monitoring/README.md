# Lab 06: Real-Time Operational Monitoring & Alerting (Prometheus & Grafana)

## Objective
Establish a complete observability and automated alerting pipeline for a real-time quick-commerce delivery operation ("Zapptto") using:
- **Prometheus Client for Python**: Emitting custom application telemetry.
- **Prometheus**: Time-series scraping engine evaluating threshold alert rules.
- **Grafana**: Dashboard visualization layer.
- **Jenkins**: CI pipeline automation via Declarative `Jenkinsfile`.

---

## Metric Architecture
Our application exposes four fundamental Prometheus metric types:

| Metric Name | Type | Description |
|---|---|---|
| `order_dispatches_total` | **Counter** | Monotonically increasing count of total orders fulfilled. |
| `current_pending_orders` | **Gauge** | Value that fluctuates up/down reflecting current waiting queue. |
| `active_riders_count` | **Gauge** | Active riders assigned to delivery runs in the field. |
| `delivery_duration_seconds` | **Summary** | Statistical distribution tracking average and percentile fulfillment time. |

---

## Instructions

### Step 1: Launch Full Stack using Docker Compose
```bash
docker compose up -d
```
This starts:
- Metrics exporter on `http://localhost:8000/metrics`
- Prometheus server on `http://localhost:9090`
- Grafana dashboard on `http://localhost:3000`

### Step 2: Validate Metric Endpoint
```bash
curl -s http://localhost:8000/metrics | grep -E "order_dispatches_total|current_pending_orders|active_riders_count"
```

### Step 3: Configure Prometheus
1. Open Prometheus UI: `http://localhost:9090`.
2. Navigate to **Status -> Targets** and ensure `zapptto_dispatch_service` displays `UP`.
3. Navigate to **Alerts** to monitor rule evaluations:
   - `HighPendingOrdersAlert`: Triggered when `current_pending_orders > 12` for 15s.
   - `CriticalDeliveryDelayAlert`: Triggered when average delivery duration exceeds 28s.

### Step 4: Configure Grafana Visualizations
1. Open Grafana: `http://localhost:3000` (Default credentials: `admin` / `admin`).
2. Add DataSource:
   - Type: **Prometheus**
   - URL: `http://prometheus:9090` (within compose) or `http://localhost:9090`
   - Click **Save & Test**.
3. Create Dashboard with Panels:
   - **Panel 1 (Stat Panel)**: `order_dispatches_total` (Total Completed Deliveries).
   - **Panel 2 (Gauge Panel)**: `current_pending_orders` (Queue Depth, Red threshold at 12).
   - **Panel 3 (Time Series)**: `active_riders_count` (Fleet in Transit).
   - **Panel 4 (Time Series)**: `delivery_duration_seconds_sum / delivery_duration_seconds_count` (Average Trip Duration).

### Step 5: Test Automated Alert Escalation
Because `metrics_server.py` simulates values between 12 and 25 for `current_pending_orders`, the condition `current_pending_orders > 12` will be continuously met. Within 15 seconds, the alert transitions in Prometheus:
`INACTIVE` ➔ `PENDING` ➔ `FIRING`.

---

## Teardown
```bash
docker compose down -v
```
