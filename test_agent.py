import asyncio

from agent.agent import agent


async def main():
    print("\nEO Geospatial Agent")
    print("Type 'exit' or 'quit' to stop.\n")

    message_history = None

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\nBye, Enjoy the rest of your day!")
            break

        if not user_input:
            continue

        try:
            result = await agent.run(
                user_input,
                message_history=message_history,
            )

            print(f"\nAgent: {result.output}\n")

            message_history = result.all_messages()

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())

