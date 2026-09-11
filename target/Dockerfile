FROM ubuntu:latest

# Vulnerabilidade IaC: Executando como usuario root por padrao
RUN apt-get update && apt-get install -y python3

COPY app.py /app/app.py

WORKDIR /app

CMD ["python3", "app.py"]

