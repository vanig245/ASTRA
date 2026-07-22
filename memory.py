from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SupportState(TypedDict):
    messages: Annotated[list[str], add_messages] #chat history
    ticket_category : str #to hold things like technical or billing etc
    resolution_draft : str # agents will write their answer
    requires_human : bool # approved or not approved by human
    QA_feedback : str # QA manager will write complaint if draft is bad
