from dataclasses import dataclass


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
        objective="Determine market attractiveness, trajectory, segmentation, and structural opportunities by combining market, competitor, customer, macro, regulatory, and geopolitical evidence.",
        research_tasks=(
            "use the competitor dossier as a starting point and validate the top 3 competitors and their relevant market positions",
            "size the relevant market only when credible public inputs support the estimate",
            "compare market trajectory, segments, geographies, customer demand, and investment signals across the company and top 3 competitors",
            "analyze technology, regulatory, macroeconomic, and geopolitical forces that could change competitive advantage or market access",
            "identify where competitor behavior reveals emerging opportunities, threats, or market white space",
        ),
        preferred_sources=("official statistics", "regulators", "government sources", "company filings", "industry associations", "primary research", "reputable geopolitical and macro sources"),
    ),
    "customer": AgentSpec(
        objective="Understand customers and unmet needs in the context of the company and its top 3 competitors.",
        research_tasks=(
            "use the competitor dossier to identify the customer segments each top competitor appears to target",
            "extract ICP and persona signals from the company and competitor propositions",
            "find voice-of-customer evidence from reviews, communities, testimonials, and case studies for the company and competitors",
            "map jobs-to-be-done, pains, desired outcomes, objections, switching triggers, and underserved segments",
            "identify where competitor customer experience or proposition leaves an unmet need",
        ),
        preferred_sources=("customer reviews", "case studies", "community discussions", "company customer pages", "product documentation", "competitor customer evidence"),
    ),
    "competitor": AgentSpec(
        objective="Build a validated competitive intelligence dossier for the company, with a ranked top 3 and enough context for downstream specialists to use it.",
        research_tasks=(
            "identify direct competitors and adjacent alternatives from independent evidence",
            "rank the top 3 competitors using relevance to the company's market, ICP, geography, product, and business model",
            "build a structured dossier for each top competitor covering positioning, ICP, products, pricing, packaging, channels, geographies, customers, strengths, weaknesses, and strategic moves",
            "identify competitor signals that require deeper market, customer, revenue, or geopolitical research",
            "identify white space, threats, switching costs, and second-order competitive effects",
        ),
        preferred_sources=("competitor official sites", "pricing pages", "product docs", "customer reviews", "company filings", "investor materials", "independent comparisons", "industry research"),
    ),
    "revenue": AgentSpec(
        objective="Diagnose monetization and pricing opportunities using the company's economics and the competitive pricing landscape.",
        research_tasks=(
            "use the competitor dossier to compare public pricing and packaging across the top 3 competitors",
            "extract public pricing and packaging for the company where available",
            "compare monetization models, value metrics, bundles, tiers, discounts, and commercial motions",
            "identify monetization, conversion, churn, expansion, and leakage hypotheses from public evidence",
            "calculate only metrics whose inputs are available and label assumptions explicitly",
        ),
        preferred_sources=("pricing pages", "billing documentation", "company filings", "investor materials", "product pages", "competitor pricing evidence"),
        tools=("web_search", "url_context", "code_execution"),
    ),
    "experiment": AgentSpec(
        objective="Turn the combined intelligence into the smallest high-learning growth experiments and prioritize them with ICE.",
        research_tasks=(
            "identify the highest-leverage uncertainty or bottleneck across the company, market, customers, competitors, and revenue evidence",
            "challenge conclusions that depend on weak or single-source evidence",
            "define measurable leading and lagging indicators",
            "design minimum viable experiments and prioritize them with ICE",
        ),
        preferred_sources=("existing agent evidence", "company product pages", "competitor evidence", "analytics documentation", "industry benchmarks"),
        tools=("web_search", "url_context", "code_execution"),
    ),
    "gtm": AgentSpec(
        objective="Build an evidence-backed go-to-market path using the company, top 3 competitors, customer intelligence, and market dynamics.",
        research_tasks=(
            "use the competitor dossier to compare ICP, positioning, channels, sales motion, partnerships, and geographic focus",
            "validate ICP from product, use cases, and customer evidence",
            "identify acquisition and distribution channels where competitors are gaining traction",
            "assess PLG, sales-led, partner, or hybrid motion fit relative to the competitive landscape",
            "identify positioning and channel white space created by competitor gaps or market shifts",
        ),
        preferred_sources=("company website", "customer stories", "competitor sites", "channel evidence", "industry research", "market research"),
    ),
}
