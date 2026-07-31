from json import load
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    max_tokens=1000,
    model='claude-haiku-4-5',
    messages=[
        {
            "role":"user",
            "content":"hey there"
        }
    ]
)

for block in message.content:
    if block.type == "text":
        print(block.text)