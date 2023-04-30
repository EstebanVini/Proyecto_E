FROM python:3.8.1-slim
WORKDIR /usr/src/app
COPY utils ./utils
COPY requirements.txt .
COPY app.py .
COPY mensajes.db .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "./app.py" ]