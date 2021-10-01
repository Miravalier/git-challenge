FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN pip install fastapi[all] uvicorn aiohttp lxml

COPY ./src /app/src
WORKDIR /app/src
CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]
