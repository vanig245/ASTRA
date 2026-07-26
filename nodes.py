import os
from memory import SupportState
from langchain_core.messages import SystemMessage
from tools import get_order_status
from tools import search_kb
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile", 
    api_key = os.environ.get("GROQ_API_KEY"),
    temperature = 0 
)

tech_llm = llm.bind_tools([search_kb])
billing_llm = llm.bind_tools([get_order_status])

def classifier_node(state : SupportState) -> dict:
    """Analyzes the user's latest message and classifies the intent."""
    messages = state["messages"]
    
    classifier_prompt = SystemMessage(content="""You are an AI triage router for a customer support system. 
Your sole job is to analyze the user's latest query and classify its intent into EXACTLY ONE of these three categories:

1. 'technical' - Queries about hardware, software troubleshooting, product repairs, or technical manuals.
2. 'billing' - Queries about order tracking, delivery status, shipping updates, or refunds.
3. 'general' - Greetings, small talk, or queries that do not fit technical or billing.

CRITICAL INSTRUCTION:
Respond with ONLY ONE word: 'technical', 'billing', or 'general'. 
Do not add any punctuation, intro text, or explanation.""")
    response = llm.invoke([classifier_prompt] + messages)
    predicted_intent = response.content.strip().lower()
    return {"intent": predicted_intent}


def technical_node(state: SupportState) -> dict:
    """Handles technical queries using the technical support specialist LLM."""
    messages = state["messages"]
    
    # TODO 8: Create a SystemMessage establishing the technical support persona.
    system_prompt = SystemMessage(content="...")
    
    # TODO 9: Invoke `tech_llm` with [system_prompt] + messages
    response = tech_llm.invoke(...)
    
    # TODO 10: Return a dictionary appending the response to the message history.
    return {"messages": [response]}


def billing_node(state: SupportState) -> dict:
    """Handles order/billing queries using the billing support specialist LLM."""
    messages = state["messages"]
    
    # TODO 11: Create a SystemMessage establishing the billing support persona.
    system_prompt = SystemMessage(content="...")
    
    # TODO 12: Invoke `billing_llm` with [system_prompt] + messages
    response = billing_llm.invoke(...)
    
    # TODO 13: Return a dictionary appending the response to the message history.
    return {"messages": [response]}