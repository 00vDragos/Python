# foloseste o imagine oficiala Python ca baza
FROM python:3.11-slim

# creeaza un director de lucru in container
WORKDIR /app

# copiaza fisierul requirements.txt in container
COPY requirements.txt .

# instaleaza pachetele Python necesare
RUN pip install --no-cache-dir -r requirements.txt

# copiaza restul fisierelor aplicatiei in container
COPY . .

# spune Docker-ului sa expuna portul Flask
EXPOSE 5000

# comanda care porneste aplicatia
CMD ["python", "run.py"]
