FROM python:3.11-slim

WORKDIR /srv

COPY . /srv

RUN pip install --no-cache-dir -r requirements.txt

ENV APP_CONFIG config.TestingConfig
RUN python -m unittest app/utests.py

EXPOSE 80 5000

ENV NAME BestMovies

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

