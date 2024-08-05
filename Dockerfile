FROM python:3.10.7-slim

WORKDIR /src/app

COPY freeze.txt freeze.txt

COPY streamlit_app.py streamlit_app.py

RUN pip install -r freeze.txt
RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["streamlit", "run",".\streamlit_app.py"]