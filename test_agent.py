import asyncio

from agent.agent import agent


async def main():
    first_result = await agent.run(
        "Which dataset should I use for NDVI at regional scale?"
    )

    print("\nFIRST RESPONSE:")
    print(first_result.output)

    second_result = await agent.run(
        "What about monthly observations?",
        message_history=first_result.all_messages(),
    )

    print("\nSECOND RESPONSE:")
    print(second_result.output)


if __name__ == "__main__":
    asyncio.run(main())