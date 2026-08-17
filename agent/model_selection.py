from pydantic_ai.capabilities import SelectModel
from pydantic_ai.models import ModelSelectionContext

from agent.model import model


def select_model(ctx: ModelSelectionContext):
    """Select the model to use for the current agent request."""

    return model


def create_model_selection_capability() -> SelectModel:
    """Create the model selection capability."""

    return SelectModel(
        selector=select_model,
        id="adaptive-model-selection",
        description="Selects the model for each agent request.",
    )