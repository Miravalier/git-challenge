FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN pip install fastapi[all] uvicorn aiohttp lxml aiofiles

COPY ./src /app/src
COPY ./static /app/src/static
WORKDIR /app/src
CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]
