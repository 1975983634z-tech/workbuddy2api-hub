# Architecture

## Components

- <code>wb_proxy.py</code>: HTTP entry point, API compatibility layer, routing, usage persistence and web assets
- <code>wb_accounts.py</code>: account model, login flows, credential refresh and upstream requests
- <code>wb_scheduler.py</code>: background maintenance and request scheduling
- <code>wb_catalog.py</code>: upstream model catalog discovery and normalization
- <code>wb_identity.py</code> / <code>wb_fingerprint.py</code>: outbound request identity helpers
- <code>wb_settings.py</code>: local settings, panel authentication, API keys and limits
- <code>wb_tasks.py</code>: optional upstream task helpers
- <code>dashboard.html</code> / <code>key-portal.html</code>: management and restricted usage interfaces
- <code>migrate_usage.py</code>: JSONL-to-SQLite migration

## Request flow

~~~mermaid
sequenceDiagram
    participant C as API client
    participant G as Gateway
    participant S as Scheduler/account pool
    participant U as Upstream service
    participant D as Usage store

    C->>G: Request with API key
    G->>G: Validate key, limits and payload
    G->>S: Select an eligible account
    S-->>G: Account and outbound proxy
    G->>U: Upstream request
    U-->>G: Stream or JSON response
    G->>D: Record sanitized usage metadata
    G-->>C: OpenAI-compatible response
~~~

## Trust boundaries

- API clients are untrusted until an API key and limits are validated.
- The management dashboard is untrusted until panel authentication succeeds.
- Upstream responses are external input and must be parsed defensively.
- <code>accounts/</code> and <code>usage/</code> contain sensitive local state and are outside the source boundary.
- Reverse proxies, TLS termination and network isolation are deployment responsibilities.

## Persistence

The gateway persists account configuration under <code>accounts/</code> and usage data under <code>usage/</code>. Source releases must keep both directories free of runtime files. Tests use temporary directories.
