from langgraph.graph import StateGraph, START, END
from memory import SupportState
from nodes import classifier_node, technical_node, billing_node, general_node
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
        return "general"
    pass


builder = StateGraph(SupportState)
builder.add_node("classifier", classifier_node)
builder.add_node("technical", technical_node)
builder.add_node("billing", billing_node)
builder.add_node("general", general_node)

builder.add_edge(START, "classifier")

builder.add_conditional_edges("classifier", intent_read)

builder.add_edge("technical", END)
builder.add_edge("billing", END)
builder.add_edge("general", END)

app = builder.compile()


if __name__ == "__main__":
    print(" Support Agent initialized!")
    chat_history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            print("bye!")
            break

        user_message = HumanMessage(content=user_input)
        chat_history.append(user_message)
        
        initial_state = {"messages": chat_history}

        final_state = app.invoke(initial_state)
        ai_response = final_state["messages"][-1].content
        print(f"Agent: {ai_response}")

        chat_history.append(final_state["messages"][-1])