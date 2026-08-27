# Grove agent architecture

Grove uses specialist research agents rather than one general-purpose analyst. Each agent has an objective, a research task set, preferred evidence sources, a bounded research loop, and a role-specific toolset.

## Market agent
- Goal: market attractiveness, trajectory, segmentation, timing, disruption.
- Research: market sizing, growth signals, macro/regulatory/technology shifts, segment opportunity, market maturity.
- Evidence: official statistics, regulators, filings, industry associations, primary research.
- Tools: Google Search + URL Context.

## Customer agent
- Goal: customer needs, behavior, friction, retention and underserved segments.
- Research: ICP/persona signals, voice of customer, reviews, communities, JTBD, objections, lifecycle signals.
- Evidence: reviews, case studies, communities, customer pages, product docs.
- Tools: Google Search + URL Context.

## Competitor agent
- Goal: competitive landscape, differentiation, white space, threats.
- Research: direct/adjacent competitors, positioning, ICP, pricing, packaging, features, channels, gaps, defensibility.
- Evidence: competitor sites, pricing pages, product docs, reviews, filings, independent comparisons.
- Tools: Google Search + URL Context.

## Revenue agent
- Goal: monetization and unit economics diagnosis.
- Research: pricing/packaging, visible funnel, conversion/churn/expansion hypotheses, revenue leakage, quantitative calculations.
- Evidence: pricing pages, billing docs, filings, investor materials, product pages.
- Tools: Google Search + URL Context + Code Execution.

## Experiment agent
- Goal: convert uncertainty into the smallest high-learning experiments.
- Research: bottleneck/uncertainty identification, impact evidence, leading/lagging metrics, MVE design, ICE prioritization.
- Evidence: upstream agent evidence, company/product evidence, analytics documentation, benchmarks.
- Tools: Google Search + URL Context + Code Execution.

## GTM agent
- Goal: evidence-backed path from ICP to positioning, channels and sales motion.
- Research: ICP validation, positioning comparison, distribution/channel evidence, PLG vs sales-led vs partner motion.
- Evidence: company sites, customer stories, competitor sites, channel evidence, industry research.
- Tools: Google Search + URL Context.

## Agentic loop

Each specialist runs up to three iterations:

1. Identify the highest-value unknowns.
2. Research using its allowed tools.
3. Separate observed evidence from inference.
4. Challenge weak or contradictory findings on subsequent iterations.
5. Stop early when the evidence threshold is met.

The loop records iteration count, queries, findings and grounding sources in `agent_trace` and `grounding_sources` so the UI can expose how an analysis was produced.

## Design principle

The model supplies reasoning; tools supply evidence and computation. Agents are not allowed to manufacture company metrics, pricing, market share, customer counts, or conversion data.
