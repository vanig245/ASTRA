import os
from memory import SupportState
from langchain_core.messages import SystemMessage
from tools import get_order_status
from tools import search_kb
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile", #decommisioned model
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
    raw_intent = response.content.strip().lower()

    if "technical" in raw_intent:
        predicted_intent = "technical"
    elif "billing" in raw_intent:
        predicted_intent = "billing"
    else:
        predicted_intent = "general"
        
    return {"intent": predicted_intent}


def technical_node(state: SupportState) -> dict:
    """Handles technical queries using the technical support specialist LLM."""
    messages = state["messages"]
    technical_prompt = SystemMessage(content= """
    You are a technical support specialist. 
    Your goal is to help users resolve technical issues, hardware problems, and product inquiries.

    Rules:
    1. Always use the search_kb tool to search the knowledge base when answering technical questions.
    2. Rely strictly on the information retrieved from search_kb. 
    3. Keep your troubleshooting steps concise, clear, and easy to follow.
    """)

    response = tech_llm.invoke([technical_prompt] + messages)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        query = tool_call["args"]["query"]
        print(f"\n[System: Searching knowledge base for '{query}'...]")

        tool_result = search_kb.invoke({"query": query})
        tool_msg = ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
        final_response = llm.invoke([technical_prompt] + messages + [response, tool_msg])
        return {"messages": [response, tool_msg, final_response]}
    return {"messages": [response]}


def billing_node(state: SupportState) -> dict:
    """Handles order/billing queries using the billing support specialist LLM."""
    messages = state["messages"]
    bill_promt = SystemMessage(content="""
    You are a billing and order support specialist. 
    Your goal is to assist customers with order status, tracking information, and shipping updates.

    Rules:
    1. If the user provides an Order ID, use the get_order_status tool immediately to query the database.
    2. If the user asks about an order but has NOT provided an Order ID, politely ask them to provide their Order ID first.
    3. Present retrieved order details cleanly to the user.
    """)

    response = billing_llm.invoke([bill_promt] + messages)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        order_id = tool_call["args"]["order_id"]
        print(f"\n[System: Querying MySQL Database for Order ID '{order_id}'...]")

        tool_result = get_order_status.invoke({"order_id": order_id})
        tool_msg = ToolMessage(content=tool_result, tool_call_id=tool_call["id"])

        final_response = llm.invoke([bill_promt] + messages + [response, tool_msg])
        return {"messages": [response, tool_msg, final_response]}
    return {"messages" : [response]}
                                
