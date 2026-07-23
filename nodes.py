from memory import SupportState

def classifier_node(state : SupportState) -> SupportState:
    message = state["messages"][-1]
    user_message = message.lower()

    for msg in state["messages"][-1]:
        if msg == "order":
            

        elif "word" and "screen" in user_message:

    
        if "refund" in user_message:
            return need_human : True
        else:
            return False