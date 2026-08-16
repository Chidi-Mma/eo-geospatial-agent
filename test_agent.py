import asyncio

from agent.agent import agent


async def main():
    user_request = (
        "Which dataset should I use for monthly precipitation at regional scale?"
    )

    result = await agent.run(
    "Which dataset should I use for monthly precipitation at regional scale?"
)

    print("\nUSER REQUEST:")
    print(user_request)

    print("\nAGENT RESPONSE:")
    print(result.output)

    print("\nMESSAGE TYPES:")
    for message in result.all_messages():
        print(type(message).__name__)


if __name__ == "__main__":
    asyncio.run(main())