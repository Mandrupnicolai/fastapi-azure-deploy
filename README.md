# fastapi-azure-deploy

> A production-ready FastAPI REST API containerized with Docker and deployed to **Azure Container Apps** via a full GitHub Actions CI/CD pipeline.

[![CI/CD](https://github.com/Mandrupnicolai/fastapi-azure-deploy/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Mandrupnicolai/fastapi-azure-deploy/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/Mandrupnicolai/fastapi-azure-deploy/branch/main/graph/badge.svg)](https://codecov.io/gh/Mandrupnicolai/fastapi-azure-deploy)
[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/Mandrupnicolai/fastapi-azure-deploy)
[![Azure](https://img.shields.io/badge/azure-container--apps-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/en-us/products/container-apps)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
=======

---

## Features

- FastAPI with automatic OpenAPI docs (`/docs`)
- Multi-stage Docker build with a non-root runtime user
- Deployed to Azure Container Apps (serverless, scale-to-zero)
- GitHub Actions pipeline: Lint -> Test -> Coverage -> Build -> Deploy
- Ruff linting + Pytest + Codecov coverage reporting
- No hardcoded secrets — all config via environment variables and GitHub Secrets

---

## Project Structure

```
fastapi-azure-deploy/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   └── routers/
│       └── health.py        # /health endpoint
├── tests/
│   └── test_health.py       # Pytest test suite
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pipeline
├── Dockerfile               # Multi-stage production build
├── pyproject.toml           # Ruff + Pytest config
└── requirements.txt
```

---

## Local Development

### Prerequisites

- Python 3.12+
- Docker

### Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the interactive API docs.

### Run with Docker

```bash
docker build -t fastapi-azure-deploy .
docker run -p 8000:8000 fastapi-azure-deploy
```

---

## Running Tests

```bash
# Run tests
pytest --tb=short

# Run tests with coverage report
pytest --tb=short --cov=app --cov-report=term-missing
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root — confirms service is live |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc API docs |

---

## CI/CD Pipeline

```
Push to main
  ├── Lint    -> Ruff checks code style and import order
  ├── Test    -> Pytest runs unit tests + uploads coverage to Codecov
  ├── Build   -> Docker image built and pushed to DockerHub
  └── Deploy  -> Azure Container Apps updated with new image SHA

Pull requests run Lint + Test only (no deploy).
```

---

## Azure Setup (one-time)

### 1. Install Azure CLI

https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

### 2. Login and provision resources (PowerShell)

```powershell
az login
az group create --name fastapi-rg --location westeurope
az monitor log-analytics workspace create --resource-group fastapi-rg --workspace-name fastapi-logs --location westeurope

$WORKSPACE_ID = az monitor log-analytics workspace show --resource-group fastapi-rg --workspace-name fastapi-logs --query customerId --output tsv
$WORKSPACE_KEY = az monitor log-analytics workspace get-shared-keys --resource-group fastapi-rg --workspace-name fastapi-logs --query primarySharedKey --output tsv

az containerapp env create --name fastapi-env --resource-group fastapi-rg --location westeurope --logs-workspace-id $WORKSPACE_ID --logs-workspace-key $WORKSPACE_KEY

az containerapp create --name fastapi-azure-deploy --resource-group fastapi-rg --environment fastapi-env --image <DOCKERHUB_USERNAME>/fastapi-azure-deploy:latest --target-port 8000 --ingress external --cpu 0.5 --memory 1.0Gi --min-replicas 0 --max-replicas 3
```

### 3. Create a Service Principal for GitHub Actions

```powershell
$SUB_ID = az account show --query id --output tsv
az ad sp create-for-rbac --name "fastapi-azure-deploy-sp" --role contributor --scopes /subscriptions/$SUB_ID/resourceGroups/fastapi-rg --sdk-auth
```

Copy the full JSON output — this is your `AZURE_CREDENTIALS` secret.

---

## GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token (Read & Write) |
| `AZURE_CREDENTIALS` | Service principal JSON |
| `AZURE_RESOURCE_GROUP` | e.g. `fastapi-rg` |
| `AZURE_CONTAINERAPP_NAME` | e.g. `fastapi-azure-deploy` |
| `CODECOV_TOKEN` | Token from codecov.io |

---

## License

MIT
