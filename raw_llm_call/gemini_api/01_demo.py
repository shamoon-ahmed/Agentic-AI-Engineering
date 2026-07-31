# a very basic example of calling gemini api

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="whats the capital of pakistan?"
)

print(response.text)
