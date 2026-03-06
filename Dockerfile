FROM python:3.12-slim

# Dependências do sistema para o Chromium
RUN apt-get update && apt-get install -y \
    curl wget gnupg \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libxshmfence1 \
    fonts-liberation xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Instala o Playwright e o Chromium
RUN pip install playwright
RUN playwright install chromium
RUN playwright install-deps chromium

RUN pip install fastapi uvicorn requests

# Instala dependências do script
RUN pip install fastapi uvicorn

WORKDIR /app
COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
