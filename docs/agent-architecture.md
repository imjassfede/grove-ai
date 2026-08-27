# Grove agent architecture

Grove is a collaborative research system, not six independent chatbots. Specialists build a shared intelligence state and can trigger targeted follow-up research after a cross-agent critique.

## Research workflow

```text
Classifier → Planner → Competitor Discovery
                         ↓
          ┌──────────────┼──────────────┐
        Market        Customer        Revenue        GTM
          └──────────────┼──────────────┘
                         ↓
                     Experiment
                         ↓
                       Critic
                    ↙          ↘
          targeted follow-up   sufficient
                    ↓             ↓
                  Critic       Synthesis
```

## Specialist responsibilities

### Competitor
Discovers and validates a ranked Top 3, then creates dossiers covering positioning, ICP, product, pricing, packaging, channels, geography, customers, strategic moves, strengths, weaknesses and competitive triggers.

### Market
Consumes the Top 3 dossier and analyzes market structure, segments, trajectory, customers, technology, regulation, macroeconomics, geography, trade and geopolitics. It looks for second-order effects and opportunities revealed by competitor behavior.

### Customer
Uses company and Top 3 competitor evidence to compare ICPs, jobs-to-be-done, pain points, objections, switching triggers, voice-of-customer signals and underserved needs.

### Revenue
Benchmarks company and Top 3 pricing/packaging, then uses code execution for defensible calculations and monetization hypotheses.

### GTM
Connects company, competitor, customer and market intelligence to ICP, positioning, channels, partnerships, geography and sales motion.

### Experiment
Turns cross-agent uncertainty into falsifiable experiments and prioritizes them with ICE.

## Agentic behavior

Every specialist has a bounded internal research loop. The cross-agent critic then checks the combined evidence for unsupported claims, contradictions, weak sources and missing information. It can delegate one targeted follow-up to the highest-value specialist for up to two additional research rounds.

## Evidence layer

Findings retain source URLs and grounding sources. The critic assigns lightweight source-quality scores and the knowledge layer builds a dependency-free JSON evidence graph of agents, findings, insights and sources. This can later move to Postgres/pgvector or a graph database without changing the agent contract.

## Memory

Prior completed analyses are retrieved through `AnalysisMemory` and supplied to new research as contextual memory. The current implementation is intentionally lightweight and can later be upgraded to semantic/vector retrieval.

## Design principle

The model provides reasoning; tools provide evidence and computation. Agents must distinguish observed facts, inferences and hypotheses and must not manufacture company metrics, pricing, market share, customer counts or conversion data.
