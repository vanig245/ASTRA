from memory import SupportState
from langchain_core.messages import SystemMessage
from tools import get_order_status
from tools import search_kb
from langchain_groq import ChatGroq

def classifier_node(state : SupportState) -> SupportState:
    message = state["messages"][-1]
    user_message = message.lower()

    # for msg in state["messages"][-1]:
    #     if msg == "order"