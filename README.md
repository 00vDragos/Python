# Math Microservice API

Aceasta aplicatie este un microserviciu scris în Python folosind Flask. 
Expune un API REST care permite calculul unor operații matematice de baza si salveaza fiecare cerere intr-o bază de date SQLite. 
Aplicatia este containerizata cu Docker pentru rulare izolata si ușoara.

## Functionalitate

- Operatii matematice implementate:
  - Putere (`pow`)
  - Factorial (`factorial`)
  - Numarul Fibonacci (`fibonacci`)
- Persistenta cererilor intr-o baza de date SQLite (`mathapi.db`)
- Autentificare si autorizare JWT (rutele de calcul sunt protejate)
- Validare cu Pydantic pentru fiecare request
- Caching in-memory cu dictionary pentru optimizarea calculelor
- Arhitectura modulara (MVC-like)
- Containerizare completa cu Docker

## Structura proiect

- `app/` – codul aplicatiei
- `models/`, `services/`, `schemas/`, `api/`
- `run.py` – punctul de pornire Flask
- `Dockerfile` – fisier de build pentru imaginea Docker
- `requirements.txt` – dependintele Python
- `mathapi.db` – baza de date generata la rulare

## Cum rulezi aplicatia(backend)

1. Construieste imaginea Docker:

```
docker build -t math-api .
```

2. Ruleaza containerul:

```
docker run -p 5000:5000 math-api
```

3. Acceseaza API-ul in browser sau Postman:

```
http://localhost:5000/api/ping
```

## Cum rulezi aplicatia – FRONTEND (React)
1. Construieste imaginea frontend:

```
docker build -t math-frontend ./math-frontend
```

2. Ruleaza containerul frontend:

```
docker run -p 5173:80 math-frontend
```
3. 
## Exemple de rute API

- `POST /api/login` – autentificare cu email si parola
- `POST /api/register` – creare cont nou
- `POST /api/fibonacci` – calcul Fibonacci
- `POST /api/factorial` – calcul factorial
- `POST /api/pow` – calcul putere
- `GET /api/history` – istoric cereri (doar cu token JWT)

## Observatii

Caching-ul este facut local cu un obiect `dict` în `MathService`. 
Baza de date este resetata daca containerul este sters, cu exceptia cazului in care se monteaza un volum separat. 


# Stan Gabriela Miruna
# Vatra Dragos