FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml .
COPY transcriber/ transcriber/

RUN pip install --no-cache-dir .

WORKDIR /data
ENTRYPOINT ["tiz-mp4-txt"]
CMD ["--help"]
