import importlib
import pkgutil

from pydantic_ai import RunContext
from pydantic_ai.toolsets import AbstractToolset, CombinedToolset

from agent import skills


def load_skills(ctx: RunContext) -> AbstractToolset | None:
    """Discover and combine available skill toolsets at runtime."""

    discovered_toolsets: list[AbstractToolset] = []

    for module_info in pkgutil.iter_modules(skills.__path__):
        module_name = module_info.name

        if module_name.startswith("_") or module_name == "loader":
            continue

        module = importlib.import_module(f"{skills.__name__}.{module_name}")

        for value in vars(module).values():
            if isinstance(value, AbstractToolset):
                discovered_toolsets.append(value)

    if not discovered_toolsets:
        return None

    return CombinedToolset(discovered_toolsets)

from pydantic_ai.toolsets import DynamicToolset

dynamic_skill_toolset = DynamicToolset(
    load_skills,
    per_run_step=False,
    id="dynamic-skills",
)