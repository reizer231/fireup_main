FROM python:3.9-slim

# Zainstaluj niezbędne pakiety systemowe
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    && rm -rf /var/lib/apt/lists/*

# Pobierz i zainstaluj Google Chrome
RUN wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome.deb \
    && rm google-chrome.deb

# Pobierz i zainstaluj ChromeDriver (automatycznie dobieramy odpowiednią wersję)
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki add-ona
COPY fireup_main.py /app/
COPY requirements.txt /app/

# Zainstaluj zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Domyślne polecenie uruchamiające skrypt
CMD [ "python", "/app/fireup_main.py" ]
