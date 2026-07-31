# calling tools with gemini API

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def weather_tool(city: str):
    return f"The weather in {city} is cloudy."

# tool = [weather_tool]

config = types.GenerateContentConfig(
    tools=[weather_tool])

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="whats the weather in islamabad?",
    config=config
)

md = list(response)

parts = response.candidates[0].content.parts[0]

print("----------------------")
print("\n=> response.candidates: ", response.candidates)
print("\n=> response.candidates[0]: ", response.candidates[0])
print("\n=> response.candidates[0].content: ", response.candidates[0].content)
print("\n=> response.candidates[0].content.parts: ", response.candidates[0].content.parts)
print("\n=> response.candidates[0].content.parts[0]: ", response.candidates[0].content.parts[0])
print("----------------------")

# if parts.function_call:

#     function = parts.function_call

#     print("Tool: ", function.name)
#     print("Args: ", function.args)

if response.function_calls:
    for call in response.function_calls:

        print("Tool: ", call.name)
        print("Args: ", call.args)

print(response.text)

print("----------------------------------------")

for m in md:
    print(m)