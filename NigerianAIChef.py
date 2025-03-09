from openai import OpenAI

client = OpenAI()

# Function to initialize system messages
def initialize_messages():
    return [
        {
            "role": "system",
            "content": (
                "You are Ayo, a lively and passionate Nigerian chef who loves to introduce people to the bold, diverse flavors of Nigerian cuisine. "
                "You share traditional recipes, cultural stories, and cooking tips with warmth and excitement, aiming to bring the vibrant spirit of "
                "Nigeria into every dish. You have deep knowledge of ingredients like yams, plantains, and a variety of Nigerian spices, and you enjoy "
                "guiding people to create authentic and flavorful dishes that reflect the rich heritage of Nigeria."
            ),
        },
        {
            "role": "system",
            "content": (
                "Respond to the user depending on their input:\n"
                "a. For ingredient-based dish suggestions: Provide only a list of dish names based on ingredients.\n"
                "b. For specific recipe requests: Give a detailed recipe with preparation steps.\n"
                "c. For critiques and improvement suggestions: Provide a constructive critique with tips for refining the dish."
            ),
        },
        {
            "role": "system",
            "content": (
                "If you do not recognize a dish, respond that you don't know it and suggest a well-known Nigerian specialty."
            ),
        }
    ]

# Initialize messages
messages = initialize_messages()

# Function to get user input and handle requests
def handle_request():
    request_type = input("Choose your request type (a: Ingredient-based dish suggestions, b: Specific recipe request, c: Recipe critique): ").strip().lower()

    if request_type == 'a':
        ingredients = input("List the ingredients you have (comma-separated):\n")
        messages.append({
            "role": "user",
            "content": f"Suggest dishes based on these ingredients: {ingredients}",
        })
    elif request_type == 'b':
        dish = input("Enter the name of the dish you want a recipe for:\n")
        messages.append({
            "role": "user",
            "content": f"Please provide a detailed recipe for {dish}",
        })
    elif request_type == 'c':
        critique_dish = input("Enter the name of the dish you want feedback on:\n")
        messages.append({
            "role": "user",
            "content": f"Please provide a critique and suggestions for improving {critique_dish}. Focus on aspects like texture, flavor, and presentation."
        })
    else:
        print("Invalid choice. Please select a, b, or c.")
        exit()

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

# Handle the initial request
handle_request()
collected_messages = call_openai_api()

# Check if any messages were collected immediately after the response
if not collected_messages:
    print("It seems I didn't provide a critique. Could you please specify what aspects you'd like feedback on?")
    critique_dish = input("Please enter the name of the dish again for feedback:\n")
    messages.append({
        "role": "user",
        "content": f"Please provide a critique and suggestions for improving {critique_dish}. Focus on aspects like texture, flavor, and presentation."
    })
    collected_messages = call_openai_api()

# Append the collected messages to the system context for future interactions
messages.append({"role": "system", "content": "".join(collected_messages)})

# After the AI responds to the initial request
while True:
    print("\n")
    user_input = input("Would you like to ask a follow-up question related to your previous request (yes/no)?\n").strip().lower()

    if user_input == 'yes':
        user_input = input("You can ask a follow-up question:\n")
        messages.append({"role": "user", "content": user_input})
        
        # Process the follow-up question
        collected_messages = call_openai_api()
        messages.append({"role": "system", "content": "".join(collected_messages)})

    elif user_input == 'no':
        # Reset the messages list for a new request
        messages = initialize_messages()

        # Ask for a new request type
        handle_request()
        collected_messages = call_openai_api()
    else:
        print("Please respond with 'yes' or 'no'.")
