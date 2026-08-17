from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import Hooks


def before_tool_execute(
    ctx: RunContext[Any],
    *,
    call,
    tool_def,
    args,
):
    print(f"\n[HOOK] Starting tool: {tool_def.name}")
    print(f"[HOOK] Arguments: {args}")

    return args


def after_tool_execute(
    ctx: RunContext[Any],
    *,
    call,
    tool_def,
    args,
    result,
):
    print(f"[HOOK] Finished tool: {tool_def.name}")
    print(f"[HOOK] Result: {result}")

    return result


def on_tool_execute_error(
    ctx: RunContext[Any],
    *,
    call,
    tool_def,
    args,
    error: Exception,
):
    print(f"[HOOK] Tool failed: {tool_def.name}")
    print(f"[HOOK] Error: {error}")


tool_execution_hooks = Hooks(
    before_tool_execute=before_tool_execute,
    after_tool_execute=after_tool_execute,
    tool_execute_error=on_tool_execute_error,
    id="tool-execution-logging",
    description="Logs dataset selection tool execution.",
)
