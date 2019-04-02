FROM python:3.6.4

RUN mkdir /app
WORKDIR /app

# INSTALL DEPENDENCIES
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "main.py"]