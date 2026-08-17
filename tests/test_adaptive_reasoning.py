import asyncio

from pydantic_ai.capabilities import Hooks

from agent.agent import agent


def test_agent_uses_adaptive_reasoning_for_simple_request():
    observed = {}

    def capture_reasoning(ctx, request_context):
        settings = request_context.model_settings

        if settings is not None:
            observed["thinking"] = settings.get("thinking")

        return request_context

    test_hooks = Hooks(
        before_model_request=capture_reasoning,
        id="test-reasoning-observer",
    )

    async def run_agent():
        return await agent.run(
            "Which dataset should I use for NDVI at regional scale?",
            capabilities=[test_hooks],
        )

    result = asyncio.run(run_agent())

    assert result.output
    assert observed["thinking"] == "low"


def test_agent_uses_medium_reasoning_for_complex_request():
    observed = {}

    def capture_reasoning(ctx, request_context):
        settings = request_context.model_settings

        if settings is not None:
            observed["thinking"] = settings.get("thinking")

        return request_context

    test_hooks = Hooks(
        before_model_request=capture_reasoning,
        id="test-medium-reasoning-observer",
    )

    async def run_agent():
        return await agent.run(
            "Compare multiple datasets for NDVI and NDMI at regional scale.",
            capabilities=[test_hooks],
        )

    result = asyncio.run(run_agent())

    assert result.output
    assert observed["thinking"] == "medium"


def test_agent_uses_high_reasoning_for_complex_global_request():
    observed = {}

    def capture_reasoning(ctx, request_context):
        settings = request_context.model_settings

        if settings is not None:
            observed["thinking"] = settings.get("thinking")

        return request_context

    test_hooks = Hooks(
        before_model_request=capture_reasoning,
        id="test-high-reasoning-observer",
    )

    async def run_agent():
        return await agent.run(
            "Compare multiple datasets for NDVI and NDMI at global scale "
            "using seasonal observations and evaluate their suitability "
            "for the analysis.",
            capabilities=[test_hooks],
        )

    result = asyncio.run(run_agent())

    assert result.output
    assert observed["thinking"] == "high"