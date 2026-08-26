# Growth AI

AI-powered Growth Intelligence Platform. Submit any business challenge — revenue, marketing, product, competitive — and receive structured root cause analysis, strategic insights, prioritised recommendations, and growth experiments on a visual canvas.

---

## What it does

| Input | Output |
| --- | --- |
| "Why is our enterprise churn increasing?" | Root causes + evidence, customer intelligence, competitive gaps, revenue levers, experiment roadmap |
| "Revenue growth slowed in Europe" | Market dynamics, regional GTM gaps, funnel analysis, P1/P2/P3 actions |
| "Activation is dropping after our onboarding update" | Behavioural insights, CRO experiments, ICE-scored hypotheses |

The platform dispatches 2–4 specialist intelligence agents in parallel, synthesises their findings, and renders the result as a navigable Growth Canvas.

---

## Architecture

```text
backend/app/
  reasoning/         ← LangGraph orchestration
    classifier.py    ← Claude classifies the problem
    planner.py       ← Claude selects which agents to run
    orchestrator.py  ← LangGraph StateGraph (parallel agent fan-out)
    evaluator.py     ← Claude synthesises all findings
    state.py         ← GrowthState TypedDict

  intelligence/      ← 6 specialist AI analysts (parallel)
    market.py        ← Market dynamics, TAM/SAM/SOM, trends
    customer.py      ← Customer behaviour, personas, churn signals
    competitor.py    ← Competitive positioning, gaps, pricing
    revenue.py       ← Funnel, CAC/LTV, unit economics
    experiment.py    ← ICE-scored growth hypotheses
    gtm.py           ← ICP, channels, positioning, messaging

  api/routes/
    analyses.py      ← POST /analyses, GET /analyses, GET /analyses/:id
  database/          ← SQLAlchemy async + PostgreSQL
  knowledge/         ← Memory layer (pgvector-ready)
  schemas/           ← Pydantic request/response models

frontend/
  app/
    page.tsx              ← Landing page
    workspace/page.tsx    ← Submit a challenge
    workspace/[id]/       ← Analysis view (canvas + report)
  components/canvas/      ← React Flow custom nodes
  lib/
    api.ts                ← API client
    canvas-layout.ts      ← Auto-positions graph nodes
    types.ts              ← Shared TypeScript types
```

---

## Local setup

### Prerequisites

- Python 3.12+
- Node.js 22+
- PostgreSQL 16 (or Docker)

### 1. Clone and configure

```bash
git clone <repo>
cd growth-ai
```

Edit `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/growthai
CORS_ORIGINS=["http://localhost:3000"]
```

### 2. Start the database

```bash
docker run -d \
  --name growthai-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=growthai \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### 3. Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

Tables are created automatically on first startup.

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:3000`.

---

## Docker Compose (full stack)

```bash
# Set your API key in backend/.env first
docker compose up --build
```

| Service | Port |
| --- | --- |
| Frontend (Next.js) | 3000 |
| Backend (FastAPI) | 8000 |
| PostgreSQL (pgvector) | 5432 |

---

## API quick reference

```bash
# Submit a challenge (triggers analysis immediately as a background task)
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{"challenge": "Why is our activation rate declining?"}'

# Poll for results (status: pending → running → complete)
curl http://localhost:8000/api/v1/analyses/<id>

# List all analyses
curl http://localhost:8000/api/v1/analyses
```

---

## MVP scope

### What works

- Full LangGraph reasoning pipeline: classify → plan → parallel agents → synthesise
- 6 intelligence agents with domain-specific Claude prompts and prompt caching
- Incremental DB persistence as the graph executes (progress visible in real time)
- Visual Growth Canvas (React Flow) with 5 custom node types
- Dual view: Canvas + structured Report tab
- 2-second polling for live status while analysis runs

### Not yet built

- Authentication / user accounts
- Persistent memory / RAG over past analyses (pgvector schema exists, retrieval not wired)
- External data integrations (CRM, GA4, ads platforms)
- Billing / usage metering
- Export to PDF / Notion / Slides

---

## Roadmap toward commercialisation

| Phase | Focus |
| --- | --- |
| v0.2 | Auth (Clerk/Auth.js), workspaces, share-by-link |
| v0.3 | RAG memory — learn from prior analyses per workspace |
| v0.4 | Data connectors — GA4, HubSpot, Stripe, LinkedIn Ads |
| v0.5 | Export (PDF report, Notion, Google Slides) |
| v0.6 | Billing (Stripe), usage limits, team seats |
| v1.0 | White-label, API access, enterprise SSO |
