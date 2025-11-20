from prometheus_client import Counter, Histogram

RPC_COUNTER = Counter("grpc_requests_total", "Total gRPC requests", ["method"])
RPC_DURATION = Histogram("grpc_request_duration_seconds",
                         "gRPC request duration", ["method"])

__all__ = ["RPC_COUNTER", "RPC_DURATION"]
