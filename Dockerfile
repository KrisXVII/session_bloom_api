FROM python:3.13-slim-bookworm
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y nano bash && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-c"]

RUN groupadd --system appgroup && useradd --system --gid appgroup --no-create-home appuser

USER appuser

COPY . .

CMD ["flask", "run"]
