# A command-line chatbot that maintains conversation history and
# uses a system prompt we wrote. We will deploy it to GitHub. 
# This is your first portfolio piece.

from google import genai
from google.genai import types

from pathlib import Path
import json
import os

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

def save_history(chat):
    
    chat_history = []

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

past_history = load_saved_history()

chat = client.chats.create(
        model='gemini-3.1-flash-lite',
        history=past_history
    )

def chatting(user_input):
    
    response = chat.send_message_stream(
        message=user_input,
        config=config
    )

    for chunk in response:
        print(chunk.text)

    # for message in chat.get_history():
    #     print("ROLE: ", message.role)
    #     print("TEXT: ", message.parts[0].text)

while True:
    user_input = input("=> YOU: ").strip()

    if not user_input:
        continue

    if user_input == "quit" or user_input == "bye":
        print("Good Bye!")
        save_history(chat)
        break

    chatting(user_input)