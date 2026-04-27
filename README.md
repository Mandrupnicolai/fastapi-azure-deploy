# fastapi-azure-deploy

> A production-ready FastAPI REST API containerized with Docker and deployed to **Azure Container Apps** via a full GitHub Actions CI/CD pipeline.

![CI/CD](https://github.com/Mandrupnicolai/fastapi-azure-deploy/actions/workflows/ci-cd.yml/badge.svg)

---

## Features

- ⚡ FastAPI with automatic OpenAPI docs (`/docs`)
- 🐳 Multi-stage Docker build with a non-root runtime user
- ☁️ Deployed to Azure Container Apps (serverless containers)
- 🔁 GitHub Actions pipeline: Lint → Test → Build → Deploy
- 🧹 Ruff linting + Pytest testing
- 🔒 No hardcoded secrets — all config via environment variables and GitHub Secrets

---

## Local Development

### Prerequisites
- Python 3.12+
- Docker

### Run locally

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

### Run with Docker

```bash
docker build -t fastapi-azure-deploy .
docker run -p 8000:8000 fastapi-azure-deploy
```

---

## Running Tests

```bash
pytest --tb=short
```

---

## Azure Setup (one-time)

### 1. Install Azure CLI
[https://learn.microsoft.com/en-us/cli/azure/install-azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

### 2. Login and create resources

```bash
az login

az group create --name fastapi-rg --location westeurope

az containerapp env create \
  --name fastapi-env \
  --resource-group fastapi-rg \
  --location westeurope

az containerapp create \
  --name fastapi-azure-deploy \
  --resource-group fastapi-rg \
  --environment fastapi-env \
  --image <DOCKERHUB_USERNAME>/fastapi-azure-deploy:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 --memory 1.0Gi \
  --min-replicas 0 --max-replicas 3
```

### 3. Create a Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "fastapi-azure-deploy-sp" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/fastapi-rg \
  --sdk-auth
```

Copy the JSON output — this is your `AZURE_CREDENTIALS` secret.

---

## GitHub Secrets Required

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `AZURE_CREDENTIALS` | Service principal JSON from `az ad sp create-for-rbac` |
| `AZURE_RESOURCE_GROUP` | e.g. `fastapi-rg` |
| `AZURE_CONTAINERAPP_NAME` | e.g. `fastapi-azure-deploy` |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root — confirm service is live |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

---

## CI/CD Pipeline
Push to main
├── Lint     → Ruff checks code style
├── Test     → Pytest runs unit tests
├── Build    → Docker image built and pushed to DockerHub
└── Deploy   → Azure Container Apps updated with new image

Pull requests run Lint + Test only (no deploy).

---

## License

MIT
