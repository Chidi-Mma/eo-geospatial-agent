from types import SimpleNamespace
from typing import cast

from pydantic_ai import RunContext
from pydantic_ai.toolsets import CombinedToolset, FunctionToolset

from agent.skills.loader import load_skills


def test_load_skills_discovers_dataset_selection_skill():
    ctx = cast(RunContext, None)

    skill = load_skills(ctx)

    assert isinstance(skill, CombinedToolset)

    dataset_skills = [
        cast(FunctionToolset, toolset)
        for toolset in skill.toolsets
        if isinstance(toolset, FunctionToolset)
        and "select_best_dataset_tool" in toolset.tools
    ]

    assert len(dataset_skills) == 1


def test_load_skills_discovers_multiple_skills(monkeypatch):
    ctx = cast(RunContext, None)

    class FakeModuleInfo:
        name = "fake_skill"

    fake_skill = FunctionToolset(
        id="fake-skill",
        instructions="A fake skill used to test dynamic discovery.",
    )

    @fake_skill.tool
    def fake_skill_tool(ctx: RunContext) -> str:
        """Return a value used to verify dynamic skill discovery."""

        return "fake skill loaded"

    def fake_iter_modules(path):
        return iter([FakeModuleInfo()])

    def fake_import_module(name):
        assert name == "agent.skills.fake_skill"

        return SimpleNamespace(fake_skill=fake_skill)

    monkeypatch.setattr("agent.skills.loader.pkgutil.iter_modules", fake_iter_modules)
    monkeypatch.setattr("agent.skills.loader.importlib.import_module", fake_import_module)

    skill = load_skills(ctx)

    assert isinstance(skill, CombinedToolset)

    tool_names = set()

    for toolset in skill.toolsets:
        if isinstance(toolset, FunctionToolset):
            tool_names.update(toolset.tools.keys())

    assert "fake_skill_tool" in tool_names