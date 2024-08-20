FROM python:3.10.7-slim

WORKDIR /src/app

COPY ./src/freeze.txt freeze.txt

COPY ./src/streamlit_app.py streamlit_app.py

RUN pip install -r freeze.txt
RUN apt-get update -y
RUN apt-get install ffmpeg -y

CMD ["streamlit", "run","streamlit_app.py"]