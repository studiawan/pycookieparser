FROM python:3.12-slim AS builder

WORKDIR /app

COPY setup.py README.md LICENSE ./
COPY pycookieparser/ ./pycookieparser/

RUN pip install --no-cache-dir .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/pycookieparser /usr/local/bin/pycookieparser

RUN mkdir -p /data/input /data/output

ENTRYPOINT ["pycookieparser"]
CMD ["--help"]
