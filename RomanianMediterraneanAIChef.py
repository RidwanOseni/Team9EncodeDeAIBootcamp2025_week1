from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

# Function to initialize system messages
def initialize_messages():
    return [
        {
            "role": "system",
            "content": (
                "You are Alex, a passionate chef who blends traditional Romanian cuisine with the healthy habits of the Mediterranean diet "
                "and the tapas culture of Spain. Your approach emphasizes fresh, high-quality ingredients sourced from Barcelona's Boquería market. "
                "You love creating dishes that are both healthy and flavorful, and you enjoy sharing tips, techniques, and cultural stories behind each recipe. "
                "You prioritize a personal touch in every cooking experience, inviting your clients to explore new tastes and improve their culinary skills."
            ),
        },
        {
            "role": "system",
            "content": (
                "Respond thoughtfully to user inquiries:\n"
                "1. Provide a detailed recipe for specific traditional dishes or fusion recipes that reflect your culinary style. "
                "2. Offer cooking tips, techniques, and suggestions to elevate the user’s cooking experience, tailored to the ingredients they have or seek.\n"
                "3. Share ideas for meals inspired by seasonal ingredients found in Mediterranean cuisine and Romanian heritage.\n"
                "4. If a dish is not recognized, suggest a well-known Romanian or Mediterranean dish they might enjoy instead."
            ),
        },
    ]

# Initialize messages
messages = initialize_messages()

# Main interaction loop
def main():
    while True:
        user_input = input("\nWhat dish or cooking technique would you like to ask about? "
                           "(or tell me anything about what kind of food you would wish to prepare "
                           "(e.g., 'I want something comforting', 'I feel like having something light and spicy'), or type 'exit' to quit):\n").strip()
        
        if user_input.lower() == 'exit':
            print("Thank you for using the Romanian Chef Assistant! Happy cooking!")
            break
        else:
            messages.append({"role": "user", "content": f"Can you suggest recipes for someone who wants to prepare: '{user_input}'?"})

        collected_messages = call_openai_api()
        
        # Check if any messages were collected
        if not collected_messages:
            print("It seems I didn't provide a response. Can you clarify what you're looking for?")
            continue

        messages.append({"role": "system", "content": "".join(collected_messages)})

# Function to call the OpenAI API and handle responses
def call_openai_api():
    model = "gpt-4o-mini"
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    return collected_messages

# Start the application
main()
