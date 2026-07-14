"""Optional AI-assisted (Layer 3) evaluators. Facilitator-only.

These wrappers use Microsoft Foundry / azure-ai-evaluation when installed. They are intentionally
optional: all attendee tracks rely only on deterministic checks + the human rubric. Import errors
are handled gracefully so the deterministic runner works without these packages.
"""
from __future__ import annotations


def ai_evaluation_available() -> bool:
    try:
        import azure.ai.evaluation  # noqa: F401
        return True
    except Exception:
        return False


def evaluate_groundedness(query: str, response: str, context: str) -> dict | None:
    """Return an AI-assisted groundedness score, or None if the SDK is unavailable/unconfigured.

    Kept as a thin, documented seam so facilitators can wire in Foundry evaluators (groundedness,
    relevance, coherence, task adherence, safety) without changing attendee-facing materials.
    """
    if not ai_evaluation_available():
        return None
    # Facilitators: instantiate the desired evaluator here with a configured model, e.g.
    #   from azure.ai.evaluation import GroundednessEvaluator
    #   return GroundednessEvaluator(model_config)(query=query, response=response, context=context)
    return None
