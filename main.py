import ollama

def chat():
    print("🤖 Conversational AI Agent (type 'exit' to quit)\n")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that remembers the conversation context."}
    ]
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(
            model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF",
            messages=messages,
        )

        # Remove the extra print statement that was printing the entire response object
        print("AI:", response["message"]["content"])

        # Add the assistant message to the messages list to maintain context
        messages.append({"role": "assistant", "content": response["message"]["content"]})

if __name__ == "__main__":
    chat()
