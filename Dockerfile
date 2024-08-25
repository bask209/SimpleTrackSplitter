FROM python:3.10.7-slim

WORKDIR /src/app

COPY ./src/freeze.txt freeze.txt

COPY ./src/simple_track_separator.py simple_track_separator.py

RUN pip install -r freeze.txt
RUN apt-get update -y
RUN apt-get install ffmpeg -y

CMD ["streamlit", "run","simple_track_separator.py"]