import sys

from react_agent import get_chain


def format_result(result):
    """Format the agent's response in a readable way"""
    if isinstance(result, dict) and 'messages' in result:
        # Extract just the assistant's response from the last message
        for message in reversed(result['messages']):
            if message['role'] == 'assistant':
                return f"\nAgent's Response:\n{'-' * 40}\n{message['content']}\n{'-' * 40}\n"

    # Fallback if the format is different
    return f"\nResult:\n{'-' * 40}\n{result}\n{'-' * 40}\n"

def main():
    print("\nWelcome to the React Agent Chat!")
    print("You can ask questions and get responses. Type 'quit' or 'exit' to end the conversation.\n")

    # Initialize the chain
    chain = get_chain()

    while True:
        # Get user input
        user_input = input("Your question: ").strip()

        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for chatting! Goodbye!\n")
            sys.exit(0)

        # Skip empty inputs
        if not user_input:
            print("Please enter a question!")
            continue

        try:
            # Format input for the chain
            inputs = {"messages": [{"role": "user", "content": user_input}]}

            # Get response from the chain
            result = chain.invoke(inputs)

            # Print formatted result
            print(format_result(result))

        except Exception as e:
            print(f"\nError occurred: {str(e)}\n")
            print("Please try again with a different question.\n")

if __name__ == "__main__":
    main()
