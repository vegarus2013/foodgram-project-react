FROM python:3.10.10-slim
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]