FROM python:3.9
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . .

CMD ["uvicorn", "conexion:app", "--host","0.0.0.0","--port","8000","--workers","4"]


