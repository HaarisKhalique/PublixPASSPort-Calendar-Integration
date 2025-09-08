FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main_direct.py schedule_processor.py schedule_uploader.py ./

ENTRYPOINT ["python", "-u", "schedule_main.py"]