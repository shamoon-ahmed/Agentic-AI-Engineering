from collections.abc import AsyncIterable
from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

items = [
    Item(name="watch", price=1200),
    Item(name="book", price=200),
    Item(name="belt", price=300)
]

# as we know streaming responses is commonly done in AI applications
# and for that we use "yield" to yield out the responses/events
# to implement that, we made a simple endpoint and yields our Item objects in the items list

# here we say -> response_class=EventSourceResponse
# and by default the FastAPI endpoint returns -> response_class=JSONResponse
# by default the FastAPI endpoint packs the dict into JSON,
# attaches Content-Type, Content-Length and sends it in one pack

# but as our endpoint yields events which can be infinite 
# and the Content-Type is "text/event-stream" and we don't know the length of the response so can't attach Content-Length
# we pass a parameter in our path parameter -> response_class=EventSourceResponse
# it sets the Content-Type to "text/event-stream" 

@app.get("/items/stream", response_class=EventSourceResponse)
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item

# when an item is yielded, in our case "item", it is encoded as JSON and sent in the "data" field of an SSE event
# like the response we get from our endpoint is:
# data: {"name":"watch","price":1200}

# data: {"name":"book","price":200}

# data: {"name":"belt","price":300}

# we can also set other fields like: data, id, comment, retry for different use cases

# data: the actual payload
# id: the event id for the browser to remember if the connection drops at "id: 4", the browser remembers it
# retry: this is the time to wait this many milliseconds before retrying
# comment: starts with a :(colon). used to keep connection alive so proxies don't close a connection sitting idle 

@app.get("/items/stream_items", response_class=EventSourceResponse)
async def items_stream() -> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(comment="sending items...")
    for i, item in enumerate(items):
        yield ServerSentEvent(
            data=item, # the actual payload ({"name":"book","price":200})
            event="item_update",
            id=i+1, # the id for the browser to remember to start from where it left off if connection drops
            retry=5000) # retry after this many milliseconds if connections drops

# Now let's see how can we resume from the last event id if the connections drops
# we pass the id in the header

@app.get("/items/stream_sse_items", response_class=EventSourceResponse)
async def sse_items(last_event_id: Annotated[int | None, Header()] = None) -> AsyncIterable[ServerSentEvent]:
    
    # this line clearly tells the browser the starting point/id to start from if the connection drops
    # so at very first interation, there's no last event id obv so it's None at the very beginning and start is 0
    start = last_event_id + 1 if last_event_id is not None else 0

    for i, item in enumerate(items):
        # now here we check if i(0) is less than start(0) which is false
        # so continue is skipped, and the event: {"name":"watch","price":1200} is yielded which has the id=0
        # now in the very next interaction, obv the last_event_id would be 0
        if i < start: 
            continue
        yield ServerSentEvent(data=item, id=str(i)) # make sure the id is wrapped in str as enumerate sends int

        # now let's say the connection dropped at that 2nd iteration
        # now when connection comes back, FastAPI sees header last_event_id = 0
        # and then start is 0 + 1 = 1
        # the for loop runs again from 0 as python is stateless/HTTP requests are stateless
        # so the i becomes 0 again and start becomes 1 
        # so according to the logic, 0 < 1 which is True so the continue lines runs, comes back to top, 
        # not the: yield ServerSentEvent(data=item, id=i) line
        # this is how the loops goes on

# mostly MCP protocols uses POST request

class Prompt(BaseModel):
    text: str

@app.post("/chat/stream", response_class=EventSourceResponse)
async def chat(prompt: Prompt) -> AsyncIterable[ServerSentEvent]:
    words = prompt.text.split()

    for word in words:
        yield ServerSentEvent(data=word, event="token")
    
    yield ServerSentEvent(raw_data="[DONE]", event="done")