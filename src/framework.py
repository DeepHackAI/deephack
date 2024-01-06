# Set up your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Define function for printing long strings as markdown
md_print = lambda text: display(Markdown(text))

# Create a chatbot class

class ChatBot:
    def __init__(self):
        # List to keep track of conversation history
        self.context = []

    def new_message(self, prompt):
        # Append user prompt to chatbot context
        self.context.append({"role": "user", "content": prompt})

        # Create assistant response
        completion = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": prompt}]
        )

        # Parse assistant response
        chat_response = completion.choices[0].message.content

        # Add assistant response to context
        self.context.append({"role": "assistant", "content": chat_response})

        # Print out conversation
        for message in self.context:
            if message["role"] == "user":
                md_print(f'User: {message["content"]}')
            else:
                md_print(f'GPT: {message["content"]}')


# Create chatbot instance
chatbot1 = ChatBot()
# Prompt
guidance_prompt ="""
You are a knowledgeable hat historian who has studied the history, styles, and proper ways to wear various types of hats. A user asks you a question about hats.
Respond to their query in a helpful and informative manner: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
guidance_prompt.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(guidance_prompt)

# Prompt
guidance_prompt ="""
You are a hat enthusiast with a wealth of knowledge about the history, styles, and etiquette of wearing various types of hats. A user is curious about hats and asks you a question. Respond to their query in a friendly and informative manner.
Respond to their query in a helpful and informative manner: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
guidance_prompt.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(guidance_prompt)

# Prompt
intension_input ="""
You are an AI that understands the nuances of hat-related queries.
Based on the user's question, determine if they are more interested in the formal history of hats or the informal style and wearing of hats.
Respond with 'Formal' for history-related queries and 'Informal' for style and wearing-related queries."
The question from user is: {USER_INPUT}
"""

# the {USER_INPUT} will be replaced by real user input.
intension_input.format(USER_INPUT="what is price of the hat?")


chatbot1.new_message(intension_input)

