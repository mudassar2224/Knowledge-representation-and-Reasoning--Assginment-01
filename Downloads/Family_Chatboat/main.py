# Console entry point for the Family Knowledge Base Chatbot.
# Run: python main.py

from aiml_bot import load_aiml
from chatbot import handle_input
from prolog_engine import load_kb


BANNER = """
============================================================
 FAMILY KNOWLEDGE BASE CHATBOT
 Powered by Pytholog + AIML
 Type 'help' for examples | Type 'quit' to exit
============================================================
"""


SAMPLE_QUERIES = [
    "hi",
    "who is Ali's father?",
    "what is Ali's dob?",
    "show siblings of Zain",
    "list children of Ali",
    "is Shakeel an ancestor of Zain?",
    "who lives in Lahore?",
    "tell me about Ali",
]


def init_bot():
    load_kb()
    load_aiml()


def main():
    print(BANNER)
    print("Initialising...")
    init_bot()
    print("\nReady! Ask me anything about the family.\n")
    print("Sample queries:")
    for query in SAMPLE_QUERIES:
        print(f"  > {query}")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Bot: Goodbye! Have a nice day.")
            break

        response = handle_input(user_input)
        print(f"\nBot: {response}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
