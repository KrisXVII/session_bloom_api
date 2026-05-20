FROM python:3.13-slim-bookworm
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --system appgroup && useradd --system --gid appgroup --no-create-home appuser

USER appuser

COPY . .

CMD ["flask", "run"]

