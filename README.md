# DevOps Mini Inventory App – End-to-End CI/CD Pipeline

Egyszerű raktárkészlet-nyilvántartó REST API (**Python + FastAPI**), amely egy teljes körűen automatizált **CI/CD pipeline-on** keresztül kerül tesztelésre, konténerizálásra és telepítésre egy saját Linux sandbox szerverre.

## Architektúra és folyamat

1. **Verziókezelés (GitHub):** A `main` branch-re érkező `push` esemény elindítja a munkafolyamatot.
2. **CI – Tesztelés (`test`):** Felhős `ubuntu-latest` runneren futó `pytest` integrációs tesztek (Quality Gate).
3. **CI – Artifact építés (`build-and-push`):** Docker image buildelése és feltöltése a **GitHub Container Registry-be (`ghcr.io`)** `latest` és commit SHA címkékkel.
4. **CD – Telepítés (`deploy`):** A sandbox szerveren (`Debian 13`) futó **GitHub Self-Hosted Runner** letölti a legfrissebb image-et, lecseréli a konténert, és `/health` smoke teszttel ellenőrzi az indulást.

## Projektstruktúra

```text
devops-mini-app/
├── .github/workflows/ci-cd.yml   # GitHub Actions CI/CD definíció
├── app/
│   ├── __init__.py
│   └── main.py                   # FastAPI alkalmazás
├── tests/
│   └── test_main.py              # Pytest tesztesetek
├── Dockerfile                    # Konténer definíció
├── requirements.txt              # Python függőségek
└── README.md
```

## API végpontok

Az interaktív Swagger UI dokumentáció futás közben a **`/docs`** útvonalon érhető el.

| Metódus | Végpont | Leírás |
| :--- | :--- | :--- |
| `GET` | `/health` | Szolgáltatás állapotának ellenőrzése (`{"status": "healthy"}`) |
| `GET` | `/items` | Aktuális raktárkészlet lekérdezése |
| `POST` | `/items/{item_id}` | Új tétel rögzítése (`name`, `quantity`) |

## Helyi futtatás és tesztelés

```bash
# Függőségek telepítése
pip install -r requirements.txt

# Tesztek futtatása
python -m pytest -v

# Alkalmazás indítása fejlesztői módban
uvicorn app.main:app --reload --port 8000
```

## Futtatás Dockerrel

```bash
# Legfrissebb image letöltése a GHCR-ből
docker pull ghcr.io/zemjanszkizoltan/devops-mini-app:latest

# Konténer indítása
docker run -d --name devops-mini-app --restart unless-stopped -p 8000:8000 ghcr.io/zemjanszkizoltan/devops-mini-app:latest
```