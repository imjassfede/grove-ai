from app.config.llm import complete
from app.reasoning.state import GrowthState

_SYSTEM = """You are a senior business strategy consultant and problem classifier.
Your role is to deeply understand a business challenge and classify it accurately
so specialist intelligence agents can be dispatched to analyze it.

You MUST respond with a valid JSON object only. No prose, no markdown fences."""

_PROMPT = """Classify this business challenge:

"{challenge}"

Return a JSON object with this exact structure:
{{
  "business_area": "<one of: marketing, sales, product, finance, strategy, operations>",
  "problem_type": "<one of: growth, retention, conversion, market, competitive, operational, product-market-fit>",
  "urgency": "<one of: critical, high, medium, low>",
  "key_questions": ["<question 1>", "<question 2>", "<question 3>", "<question 4>", "<question 5>"],
  "context_signals": ["<brief signal extracted from the challenge>"]
}}

key_questions must be the 5 most important diagnostic questions needed to solve this challenge.
context_signals are specific facts or signals mentioned in the challenge text."""


async def classify(state: GrowthState) -> dict:
    data = await complete(_SYSTEM, _PROMPT.format(challenge=state["challenge"]))

    return {
        "business_area": data["business_area"],
        "problem_type": data["problem_type"],
        "urgency": data["urgency"],
        "key_questions": data["key_questions"],
        "status": "planning",
        "progress": [f"Problem classified: {data['business_area']} / {data['problem_type']} (urgency: {data['urgency']})"],
    }
