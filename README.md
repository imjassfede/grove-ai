# Grove

**AI-powered Strategic Intelligence**

> One business problem. Multiple AI perspectives. One strategic answer.

Grove is an experimental multi-agent AI system for turning complex business challenges into structured analysis, strategic insights, prioritised recommendations, and actionable experiments.

Instead of asking a single general-purpose model for a generic answer, Grove decomposes a business problem, selects the most relevant specialist perspectives, runs analyses in parallel, and synthesises the findings into one strategic view.

## Why Grove

Business problems rarely belong to one function.

A question about declining revenue may require market context, customer behaviour, competitive intelligence, unit economics, go-to-market analysis, and experimentation.

Grove explores what happens when these perspectives become specialised AI agents that can reason together.

## How it works

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

## Specialist intelligence layers

| Agent | Focus |
| --- | --- |
| **Market** | Market dynamics, TAM/SAM/SOM, trends |
| **Customer** | Customer behaviour, personas, churn signals |
| **Competitor** | Competitive positioning, gaps, pricing |
| **Revenue** | Funnel, CAC/LTV, unit economics |
| **Experiment** | Growth hypotheses and prioritisation |
| **GTM** | ICP, channels, positioning, messaging |

The system is designed so that not every problem needs every agent. Grove first determines which perspectives are relevant, then orchestrates the analysis accordingly.

## What Grove produces

For a business challenge, Grove aims to produce:

- structured multi-perspective analysis
- key findings and signals
- prioritised recommendations
- growth and business experiments
- a visual intelligence workspace
- a structured report that can be reviewed by a human decision-maker

The goal is not to replace human judgement. It is to make the reasoning process faster, more structured, and easier to explore.

## Architecture

### Current stack

- **Python / FastAPI** — backend API
- **LangGraph** — agent orchestration and reasoning workflow
- **Gemini 2.5 Flash** — LLM layer
- **PostgreSQL + pgvector** — persistence and future memory layer
- **React / Next.js** — frontend
- **React Flow** — visual intelligence canvas
- **Docker Compose** — local full-stack environment

The LLM layer is isolated behind a provider interface so Grove can evolve toward a model-agnostic architecture without coupling the reasoning workflow to a single provider.

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

## Roadmap

| Phase | Focus |
| --- | --- |
| **v0.2** | Authentication, workspaces, shareable analyses |
| **v0.3** | Persistent memory and RAG |
| **v0.4** | Business data connectors — GA4, HubSpot, Stripe, LinkedIn Ads |
| **v0.5** | Export to PDF, Notion and Google Slides |
| **v0.6** | Billing, usage limits and team seats |
| **v1.0** | Enterprise capabilities, API access and white-labeling |

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

## Project status

Grove is an early-stage experimental project exploring how multi-agent AI systems can move beyond generic chat responses and become practical interfaces for business reasoning and decision support.

The project is being built iteratively, with the architecture and product assumptions evolving alongside each experiment.

## Build in public

Grove is also a practical experiment in building AI products in public: testing architectures, evaluating agent workflows, connecting business data, and documenting what actually works.

More experiments and implementation details will be shared as the project evolves.
