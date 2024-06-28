
```mermaid
graph TD;
    A[User (through web API or telegram bot)] -->|REST: list, ticker (SBER, GAZP, etc..)| B[DividendCounter Manager];
    B -->|REST: get_instruments, get_prices| C[TCS API Accessor (R/O)];
    C --> D[TCS API];
    B -->|Queue: save report| E[Log Accessor];
    E --> F[Log file];
    B -->|gRPC: save_instruments, get_by_ticker, list, PutQueue, GetQueue| G[RedisAccessor (stores K:V, provides Queue)];
    G --> H[Redis];
```
