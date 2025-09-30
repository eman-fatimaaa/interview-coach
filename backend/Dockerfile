FROM python:3.13-slim

WORKDIR /app

# install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

# expose
EXPOSE 8000

# run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
