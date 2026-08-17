from typing import Any, Literal

from pydantic_ai import RunContext
from core.schemas import DatasetSelectionRequest

from pydantic_ai.capabilities import Thinking


ReasoningLevel = Literal["low", "medium", "high"]


def determine_reasoning_level(
    request: DatasetSelectionRequest,
) -> ReasoningLevel:
    """Determine the reasoning effort required for a dataset selection request."""

    complexity_score = 0

    # Multiple required bands or variables increase reasoning complexity.
    if len(request.required_bands) >= 2:
        complexity_score += 1

    if len(request.required_variables) > 1:
        complexity_score += 1

    # More complex spatial scopes require more consideration.
    if request.spatial_scale in {"continental", "global"}:
        complexity_score += 1

    # Seasonal and annual requirements can require more temporal reasoning.
    if request.temporal_requirement in {"seasonal", "annual"}:
        complexity_score += 1

    # Multi-requirement descriptions indicate a potentially more complex request.
    if request.description:
        description_length = len(request.description.split())

        if description_length > 30:
            complexity_score += 1

    if complexity_score >= 3:
        return "high"

    if complexity_score >= 1:
        return "medium"

    return "low"



def determine_reasoning_from_prompt(prompt: str) -> ReasoningLevel:
    """Estimate reasoning effort from the complexity of a user prompt."""

    prompt_lower = prompt.lower()
    complexity_score = 0

    # Explicit comparison or multiple-analysis requests.
    if any(
        term in prompt_lower
        for term in [
            "compare",
            "comparison",
            "multiple datasets",
            "multiple requirements",
            "several requirements",
        ]
    ):
        complexity_score += 1

    # Broader spatial scopes require more consideration.
    if any(
        term in prompt_lower
        for term in [
            "continental",
            "global",
            "worldwide",
        ]
    ):
        complexity_score += 1

    # More complex temporal requirements.
    if any(
        term in prompt_lower
        for term in [
            "seasonal",
            "annual",
            "yearly",
            "long-term",
        ]
    ):
        complexity_score += 1

    # Longer prompts are more likely to contain multiple requirements.
    if len(prompt.split()) > 30:
        complexity_score += 1

    if complexity_score >= 3:
        return "high"

    if complexity_score >= 1:
        return "medium"

    return "low"


def create_thinking_capability(
    reasoning_level: ReasoningLevel,
) -> Thinking:
    """Create a Thinking capability matching the requested reasoning level."""

    return Thinking(
        effort=reasoning_level,
        id="adaptive-reasoning",
        description="Adjusts model reasoning effort based on request complexity.",
    )



def adaptive_reasoning_capability(
    ctx: RunContext[Any],
):
    """Create a thinking capability based on the current user prompt."""

    prompt = ctx.prompt

    if isinstance(prompt, str):
        reasoning_level = determine_reasoning_from_prompt(prompt)
    else:
        reasoning_level = "low"

    return create_thinking_capability(reasoning_level)