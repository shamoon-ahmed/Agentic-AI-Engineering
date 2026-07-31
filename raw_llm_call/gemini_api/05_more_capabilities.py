from google import genai
from google.genai import types

from PIL import Image

from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

# system instructions example

system_instructions = "Respond very briefly like a cat"

config = types.GenerateContentConfig(system_instruction=system_instructions)

response = client.models.generate_content_stream(
    model='gemini-3.1-flash-lite',
    contents="how to pronounce the word pronounciation?",
    config=config
)

for chunk in response:
    print(chunk.text)

# thinking feature configuration example

# thinking is already enabled by default. 
# here we are configuring it like low, high etc.
config2 = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level='low')
)

#  multimodal example

image = Image.open("C:\Agentic-AI-Engineering\ChatGPT Image Jul 28, 2026, 11_06_57 PM.png")

response = client.models.generate_content(
    model='gemini-3.1-flash-lite',
    contents=[image, 'whats the text in this image?']
)

# print(response.text)