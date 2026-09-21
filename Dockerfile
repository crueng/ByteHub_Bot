FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/crueng/ByteHub_Bot"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    BYTEHUB_DATA_DIR=/data \
    BYTEHUB_LOGS_DIR=/logs \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 bytehub \
    && mkdir -p /app /data /logs /opt/venv \
    && chown bytehub:bytehub /app /data /logs /opt/venv

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh

USER bytehub

RUN python -m venv /opt/venv

COPY --chown=bytehub:bytehub requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

WORKDIR /app

ENTRYPOINT ["entrypoint.sh"]
CMD ["python", "-m", "ByteHub"]