FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements-dev.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM builder AS test
WORKDIR /src
COPY . .
CMD ["pytest", "-v"]

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN groupadd --system app && useradd --system --gid app --no-create-home app \
 && mkdir /data && chown app:app /data
WORKDIR /srv
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY core ./core
COPY adapters ./adapters
COPY config ./config
COPY main.py ./main.py
RUN chown -R app:app /srv
USER app
EXPOSE 8081
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=5 \
  CMD python -c "import os,urllib.request;urllib.request.urlopen('http://127.0.0.1:%s/health' % os.getenv('PORT','8081'),timeout=2)" || exit 1
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8081} --workers 1 --threads 4 'main:wsgi()'"]
