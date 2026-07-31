# how to stream the AI response chunk by chunk

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-3.1-flash-lite",
    contents="write a 10 line poem on trees"
)

for chunks in response:
    print(chunks)

print("---------------------------------------")

for chunks in response:
    print(chunks.text, end="", flush=True) 

# end="" enables word to print side by side instead of python forcing it to be printed on a new line everytime
# flush=True forces the chunks to be actually printed on the terminal no matter what, because terminals saves 
# computer's resources and waits until the whole text is generated (this is called buffering)
