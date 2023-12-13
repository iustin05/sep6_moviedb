FROM python:3.11-slim

WORKDIR /srv

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gnupg \
        apt-transport-https \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB3E94ADBE1229CF

RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /srv

RUN pip install --no-cache-dir -r requirements.txt

ENV APP_CONFIG config.TestingConfig
RUN python -m unittest app/utests.py

EXPOSE 80 5000

ENV NAME BestMovies

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

