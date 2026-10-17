from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SupportState(TypedDict):
    messages: Annotated[list, add_messages] #chat history
    intent : str #to hold things like technical or billing etc
