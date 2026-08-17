import asyncio

from agent.agent import agent


def test_agent_preserves_conversation_state():
    async def run_conversation():
        first_result = await agent.run(
            "Which dataset should I use for NDVI at regional scale?"
        )

        second_result = await agent.run(
            "What about monthly observations?",
            message_history=first_result.all_messages(),
        )

        return second_result.output

    response = asyncio.run(run_conversation()).lower()

    assert "modis" in response
    assert "monthly" in response