# 1. Bazowy obraz
FROM python:3.11

# 2. Ustaw katalog roboczy
WORKDIR /app

# 3. Skopiuj zależności (upewnij się że masz requirements.txt)
COPY requirements.txt .

# 4. Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# 5. Skopiuj cały projekt
COPY . .

# 6. Komenda uruchamiająca
CMD ["daphne", "-b", "0.0.0.0", "-p", "3000", "corptalk.asgi:application"]
