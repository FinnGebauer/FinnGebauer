FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "etl.py"]