# A command-line chatbot that maintains conversation history and
# uses a system prompt we wrote. We will deploy it to GitHub. 
# This is my first portfolio piece.

from google import genai
from google.genai import types

from pathlib import Path
import json

from dotenv import load_dotenv

load_dotenv()

HISTORY_FILE = Path("chat_history.json")

client = genai.Client()

system_instructions = """
You are a friendly kitten who speaks like a cat. 
Your name is Tinku. Do not imitate humans. Answer very briefly
"""

config = types.GenerateContentConfig(
    system_instruction=system_instructions,
    thinking_config=types.ThinkingConfig(thinking_level='medium')
)

# whenever user quits (says quit or bye), the conversation history saves of that chat
def save_history(chat):
    
    chat_history = []

    # as chat messages has types.Content() objects which is the way gemini API reads it
    # we don't save it in the same manner. Instead we save the json file with role and text
    for messages in chat.get_history():
        text_content = "".join([part.text for part in messages.parts if part.text])
        role = messages.role

        chat_history.append(
            {
                "role":role,
                "text":text_content
            }
        )

    with open(HISTORY_FILE, 'w') as hf:
        json.dump(chat_history, hf, indent=2)

# here we are loading the pre-saved history (if it exists)
# as the chat_history.json contains json schema, not the types.Content() objects,
# we convert that json back into the form the Gemini API can read, the types.Content() objects
def load_saved_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, 'r') as hf:
            saved_history = json.load(hf)

            history = []
            for item in saved_history:
                history.append(
                    types.Content(
                        role=item['role'],
                        parts=[types.Part.from_text(text=item["text"])]
                )
            )
            return history

    except Exception as e:
        print("Cannot load history!")
        return []

# loading pre-saved history
past_history = load_saved_history()

# creating a chat and passing the pre-saved history
chat = client.chats.create(
        model='gemini-3.1-flash-lite',
        history=past_history
    )

# creating chatting function that sends message and prints response chunk by chunk
def chatting(user_input):

    response = chat.send_message_stream(
        message=user_input,
        config=config
    )
    
    print("=> AI: ")
    for chunk in response:
        print(chunk.text)

    # for message in chat.get_history():
    #     print("ROLE: ", message.role)
    #     print("TEXT: ", message.parts[0].text)

# here we use a while loop that runs until user says quit or bye
# after they say quit or bye, the save_history() saves the conversation
while True:
    user_input = input("=> YOU: ").strip()

    if not user_input:
        continue

    if user_input == "quit" or user_input == "bye":
        print("Good Bye!")
        save_history(chat)
        break

    chatting(user_input)