import asyncio

from agent.agent import agent


def test_agent_tool_execution_hooks(capsys):
    async def run_agent():
        return await agent.run(
            "Which dataset should I use for NDVI at regional scale?"
        )

    result = asyncio.run(run_agent())

    assert result.output

    captured = capsys.readouterr().out

    assert "[HOOK] Starting tool: select_best_dataset_tool" in captured
    assert "[HOOK] Arguments:" in captured
    assert "[HOOK] Finished tool: select_best_dataset_tool" in captured
    assert "[HOOK] Result:" in captured
