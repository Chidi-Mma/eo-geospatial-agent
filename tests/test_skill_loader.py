from typing import cast

from pydantic_ai import RunContext
from pydantic_ai.toolsets import CombinedToolset, FunctionToolset

from agent.skills.loader import load_skills


def test_load_skills_discovers_dataset_selection_skill():
    ctx = cast(RunContext, None)

    skill = load_skills(ctx)

    assert isinstance(skill, CombinedToolset)
    assert len(skill.toolsets) == 1

    dataset_skill = cast(FunctionToolset, skill.toolsets[0])

    assert "select_best_dataset_tool" in dataset_skill.tools