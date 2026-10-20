# WorkBuddy Multi-Account Reverse Proxy Gateway
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=8788 API_KEY= TZ=Asia/Shanghai

WORKDIR /app

RUN apk add --no-cache tzdata ca-certificates && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    pip install --no-cache-dir urllib3

COPY wb_*.py migrate_usage.py *.html ./
RUN mkdir -p /app/accounts /app/usage

VOLUME ["/app/accounts", "/app/usage"]
EXPOSE 8788

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/health' % os.environ.get('PORT','8788'), timeout=3)" || exit 1

CMD ["python", "wb_proxy.py", "--host", "0.0.0.0", "--lan"]
