from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentSpec:
    objective: str
    research_tasks: tuple[str, ...]
    preferred_sources: tuple[str, ...]
    tools: tuple[str, ...] = ("web_search", "url_context")
    max_iterations: int = 3
    min_findings: int = 3


AGENT_SPECS: dict[str, AgentSpec] = {
    "market": AgentSpec(
        objective="Determine market attractiveness, trajectory, segmentation, and structural opportunities.",
        research_tasks=(
            "size the relevant market only when credible public inputs support the estimate",
            "identify current growth, demand, technology, regulatory, and macro signals",
            "map meaningful segments and identify where opportunity is concentrated",
            "identify market maturity, timing, and disruption risks",
        ),
        preferred_sources=("official statistics", "regulators", "company filings", "industry associations", "primary research"),
    ),
    "customer": AgentSpec(
        objective="Understand who the customer is, what they value, and where friction or unmet needs exist.",
        research_tasks=(
            "extract ICP and persona signals from the company proposition",
            "find voice-of-customer evidence from reviews, communities, testimonials, and case studies",
            "map jobs-to-be-done, pains, desired outcomes, and objections",
            "identify lifecycle, retention, churn, and underserved-segment signals",
        ),
        preferred_sources=("customer reviews", "case studies", "community discussions", "company customer pages", "product documentation"),
    ),
    "competitor": AgentSpec(
        objective="Map the competitive landscape and identify differentiated white space and threats.",
        research_tasks=(
            "identify direct and adjacent competitors from independent evidence",
            "compare positioning, ICP, product scope, pricing, packaging, and channels",
            "identify competitor strengths, weaknesses, and meaningful gaps",
            "assess differentiation, switching costs, and defensibility",
        ),
        preferred_sources=("competitor official sites", "pricing pages", "product docs", "customer reviews", "filings", "independent comparisons"),
    ),
    "revenue": AgentSpec(
        objective="Diagnose monetization and unit economics, separating known metrics from assumptions.",
        research_tasks=(
            "extract public pricing and packaging where available",
            "reconstruct the visible acquisition-to-revenue funnel from public evidence",
            "identify monetization, conversion, churn, expansion, and leakage hypotheses",
            "calculate only metrics whose inputs are available and label assumptions explicitly",
        ),
        preferred_sources=("pricing pages", "billing documentation", "company filings", "investor materials", "product pages"),
        tools=("web_search", "url_context", "calculator"),
    ),
    "experiment": AgentSpec(
        objective="Turn evidence and uncertainty into the smallest high-learning growth experiments.",
        research_tasks=(
            "identify the highest-leverage uncertainty or bottleneck",
            "find evidence for expected impact and implementation constraints",
            "define measurable leading and lagging indicators",
            "design minimum viable experiments and prioritize them with ICE",
        ),
        preferred_sources=("existing agent evidence", "company product pages", "analytics documentation", "industry benchmarks"),
        tools=("web_search", "url_context", "calculator"),
    ),
    "gtm": AgentSpec(
        objective="Build an evidence-backed go-to-market path from ICP through positioning, channels, and sales motion.",
        research_tasks=(
            "infer and validate ICP from product, use cases, and customer evidence",
            "compare positioning and messaging against alternatives",
            "identify acquisition and distribution channels used by the category",
            "assess PLG, sales-led, partner, or hybrid motion fit",
        ),
        preferred_sources=("company website", "customer stories", "competitor sites", "channel evidence", "industry research"),
    ),
}
