FROM python:3.11-slim

WORKDIR /app

COPY AI_Risk_Surveillance/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY AI_Risk_Surveillance ./

ENV PORT=10000
EXPOSE 10000

CMD ["python", "app.py"]