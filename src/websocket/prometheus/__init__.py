from prometheus_client import Counter, Gauge, Histogram

WS_CONNECTIONS = Gauge(
    "ws_connections",
    "Active WebSocket connections"
)

WS_MESSAGES_TOTAL = Counter(
    "ws_messages_total",
    "Total WebSocket messages processed",
    ["event"]
)

WS_ERRORS_TOTAL = Counter(
    "ws_errors_total",
    "Total WebSocket errors",
    ["event"]
)

WS_EVENT_DURATION = Histogram(
    "ws_event_duration_seconds",
    "WebSocket event handler duration",
    ["event"]
)
