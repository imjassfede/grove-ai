# Grove

**AI-powered Strategic Intelligence**

Grove is an experimental AI system for turning complex business challenges into structured analysis, strategic insights, prioritised recommendations, and actionable experiments.

Instead of relying on a single general-purpose answer, Grove routes a business challenge to specialist intelligence agents, runs relevant analyses in parallel, synthesises their findings, and presents the result through a visual workspace.

> **One business problem. Multiple AI perspectives. One strategic answer.**

---

## What it does

Give Grove a challenge such as:

- "Why is our enterprise churn increasing?"
- "Revenue growth slowed in Europe. What should we investigate?"
- "Activation is dropping after our onboarding update. Where should we look?"

Grove classifies the problem, selects the most relevant specialist perspectives, runs them in parallel, and combines the findings into a structured strategic analysis.

### Specialist intelligence layers

| Agent | Focus |
| --- | --- |
| Market | Market dynamics, TAM/SAM/SOM, trends |
| Customer | Customer behaviour, personas, churn signals |
| Competitor | Competitive positioning, gaps, pricing |
| Revenue | Funnel, CAC/LTV, unit economics |
| Experiment | Growth hypotheses and prioritisation |
| GTM | ICP, channels, positioning, messaging |

---

## Architecture

```text
Business Challenge
       ↓
Problem Classification
       ↓
Analysis Planning
       ↓
┌──────┴──────┬──────────┬──────────┐
Market     Customer   Competitor  Revenue
└──────┬──────┴──────────┴──────────┘
       ↓
GTM + Experiment Analysis
       ↓
Synthesis & Evaluation
       ↓
Strategic Insight
       ↓
Visual Intelligence Canvas
```

### Current stack

- **Python / FastAPI** — backend API
- **LangGraph** — reasoning and agent orchestration
- **Gemini 2.5 Flash** — LLM layer
- **PostgreSQL + pgvector** — persistence and future memory layer
- **React / Next.js** — frontend
- **React Flow** — visual intelligence canvas
- **Docker Compose** — local full-stack environment

The LLM layer is intentionally isolated behind a small provider interface so the reasoning system can evolve independently from the underlying model provider.

---

## Current MVP

### Working

- Business challenge classification
- Dynamic specialist-agent selection
- Parallel intelligence analysis
- Strategic synthesis
- Incremental analysis persistence
- Visual intelligence canvas
- Structured report view
- Live analysis status

### In development

- Persistent memory / RAG across analyses
- Authentication and workspaces
- External business-data connectors
- Export to business documents
- Usage and billing infrastructure

---

## Roadmap

| Phase | Focus |
| --- | --- |
| v0.2 | Authentication, workspaces, shareable analyses |
| v0.3 | Persistent memory and RAG |
| v0.4 | Business data connectors — GA4, HubSpot, Stripe, LinkedIn Ads |
| v0.5 | Export to PDF, Notion and Google Slides |
| v0.6 | Billing, usage limits and team seats |
| v1.0 | Enterprise capabilities, API access and white-labeling |

---

## Local development

### Prerequisites

- Python 3.12+
- Node.js 22+
- PostgreSQL 16, or Docker

### Configure the backend

Create `backend/.env`:

```env
GOOGLE_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/growthai
CORS_ORIGINS=["http://localhost:3000"]
```

### Start the database

```bash
docker run -d \
  --name grove-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=growthai \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Or run the full stack with:

```bash
docker compose up --build
```

---

## Project status

Grove is an early-stage experimental project. The goal is to explore how multi-agent AI systems can move beyond generic chat responses and become practical interfaces for business reasoning and decision support.

Built in public as the architecture evolves.
