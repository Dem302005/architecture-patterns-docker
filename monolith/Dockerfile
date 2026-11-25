FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements-dev.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM builder AS test
WORKDIR /src
COPY app ./app
COPY tests ./tests
CMD ["pytest", "-v", "tests/domain", "tests/application", "tests/test_architecture.py"]

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN groupadd --system app && useradd --system --gid app --no-create-home app
WORKDIR /srv
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY app ./app
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh && chown -R app:app /srv
USER app
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=5 \
  CMD python -c "import os,urllib.request;urllib.request.urlopen('http://127.0.0.1:%s/health' % os.getenv('PORT','8080'),timeout=2)" || exit 1
ENTRYPOINT ["./entrypoint.sh"]
