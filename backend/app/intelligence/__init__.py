from app.intelligence.competitor import CompetitorIntelligenceAgent
from app.intelligence.customer import CustomerIntelligenceAgent
from app.intelligence.experiment import ExperimentIntelligenceAgent
from app.intelligence.gtm import GTMIntelligenceAgent
from app.intelligence.market import MarketIntelligenceAgent
from app.intelligence.revenue import RevenueIntelligenceAgent

registry: dict = {
    "market": MarketIntelligenceAgent(),
    "customer": CustomerIntelligenceAgent(),
    "competitor": CompetitorIntelligenceAgent(),
    "revenue": RevenueIntelligenceAgent(),
    "experiment": ExperimentIntelligenceAgent(),
    "gtm": GTMIntelligenceAgent(),
}

__all__ = ["registry"]
