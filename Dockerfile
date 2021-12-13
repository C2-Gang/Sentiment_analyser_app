FROM python:3.6

COPY /app/. /app
COPY app/app.py /app
COPY app/__main__.py /app
COPY app/__init__.py /app
COPY /models/. /app/models
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt

ENV FLASK_APP=app/app.py
EXPOSE 5000:5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]