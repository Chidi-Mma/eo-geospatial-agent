from typing import cast

from agent.model import model
from agent.model_selection import (
    create_model_selection_capability,
    select_model,
)
from pydantic_ai.capabilities import SelectModel
from pydantic_ai.models import ModelSelectionContext


def test_select_model_returns_configured_model():
    context = cast(ModelSelectionContext, object())

    assert select_model(context) is model


def test_create_model_selection_capability():
    capability = create_model_selection_capability()

    assert isinstance(capability, SelectModel)
    assert capability.id == "adaptive-model-selection"
    assert capability.selector is select_model