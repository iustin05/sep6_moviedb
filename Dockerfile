FROM python:3.11-slim

WORKDIR /srv

COPY . /srv

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m unittest app/utests.py

EXPOSE 80 5000

ENV NAME BestMovies

CMD ["python", "app/run.py"]
