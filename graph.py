from langgraph.graph import StateGraph, START, END
from memory import SupportState
from nodes import classifier_node, technical_node, billing_node
from langchain_core.messages import HumanMessage

def intent_read(state: SupportState) -> str:
    """
    Reads the 'intent' field from the state (set by classifier_node) 
    and returns the string name of the next node to run.
    """
    intent = state.get("intent", "general")
    if intent == "technical":
        return "technical"
    elif intent == "billing":
        return "billing"
    else:
        return END
    pass


builder = StateGraph(SupportState)
builder.add_node("classifier", classifier_node)
builder.add_node("technical", technical_node)
builder.add_node("billing", billing_node)

builder.add_edge(START, "classifier")

builder.add_conditional_edges("classifier", intent_read)

builder.add_edge("technical", END)
builder.add_edge("billing", END)

app = builder.compile()