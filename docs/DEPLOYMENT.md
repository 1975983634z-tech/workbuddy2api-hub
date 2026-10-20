# Deployment

## Local-only

~~~bash
python3 wb_proxy.py   --host 127.0.0.1   --port 8788   --panel-password '<change-me>'
~~~

This is the safest default. The panel is reachable only from the local machine.

## Docker

~~~bash
docker compose up -d --build
docker compose logs -f wb-proxy
~~~

Persistent directories:

- <code>./accounts</code>
- <code>./usage</code>

Back them up only through an encrypted channel. Do not place them in Git, release archives or public cloud folders.

## LAN

~~~bash
python3 wb_proxy.py --lan --port 8788 --panel-password '<change-me>'
~~~

Restrict the port to a trusted subnet and rotate the generated API key if it is exposed.

## Public deployment

Put the gateway behind a reverse proxy that provides:

- HTTPS with a valid certificate
- Authentication and source-address restrictions
- Rate limiting and request-size limits
- Access logs with tokens and authorization headers redacted
- Timeouts compatible with streaming responses

Do not publish the account-management panel to the public internet unless you have reviewed and tested the complete security model.
