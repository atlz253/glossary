FROM golang:1.24 AS builder

WORKDIR /src

RUN go install go.k6.io/xk6/cmd/xk6@v1.2.6

RUN xk6 build --output /k6 --with github.com/Hyperspace-Metaverse/xk6-socketio@latest

FROM grafana/k6:1.3.0

COPY --from=builder /k6 /usr/bin/k6
