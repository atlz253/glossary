FROM golang:1.24 AS builder
WORKDIR /app
RUN go install go.k6.io/xk6/cmd/xk6@latest
RUN xk6 build --with github.com/grafana/xk6-dashboard

FROM alpine
COPY --from=builder /app/k6 /usr/local/bin/k6
ENTRYPOINT k6 run --out dashboard $TEST_FILE