# in the previous examples, everytime we send a query, its new for the llm
# the multi-turn chat makes a history and appends the user prompt and AI response in the history list
# the AI now remembers what was said in the last prompt

from google import genai
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = genai.Client()

chat = client.chats.create(model="gemini-3.1-flash-lite")

def chatting(user_input: str):
    response = chat.send_message(user_input)

    print("AI: ", response.text)

while True:
    query = input("USER: ").strip() # .strip() removes the extra white spaces from both ends

    if not query:
        continue

    if query == "quit" or query == "bye":
        break

    chatting(query)

# query1 = "what color are apples generally??"
# print("USER => ", query1)

# response1 = chat.send_message(query1)
# print("AI => ", response1.text)

# query2 = "what about oranges?"
# print("USER => ", query2)

# response2 = chat.send_message(query2)
# print("AI => ", response2.text)

# ----------------------------------------------

# async def chatting(user_input: str):
#     response = await chat.send_message(user_input)

#     print("AI: ", response)

# async def main():
#     while True:
#         query = input("USER: ").strip() # .strip() removes the extra white spaces from both ends

#         if not query:
#             continue

#         if query == "quit" or query == "bye":
#             break

#         chat = chatting(query)

#         await chat


# asyncio.run(main())