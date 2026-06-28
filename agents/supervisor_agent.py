from typing import Literal
from state import analyst_state
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field
from langchain_core.messages import HumanMessage,SystemMessage

sys_prompt = """
# identity : 
                your are an supervisor agent.
# instructions                
                    you have two workers:
                    
                    1. sql_agent description : (capable of writing and executing sql_queries.)
                    2. visualize_agent description : (capable of writing and executing data visualization codes by it self in seaborn.) 
                
                look at the user's request and conversation history:
                    
                    1. if a worker is needed, route to them.
                    2. if user's request has been fulfilled by the workers, route to end.

"""
future = """and describe the users's request more precisely and effectively to get the maximum results.
                    NOTE: if there is a need to call visualize_agent, then make sure to describe the user's intent or your intent of how the graph need to look like to get a wonderful graph.    
"""

class desicion_schema(BaseModel):
    """decide wich agent to call next or Finish the conversation"""
    next : Literal["sql_agent","visualize_agent","Finish"]
    
llm = init_chat_model(model="groq:openai/gpt-oss-120b")
supervisor_llm = llm.with_structured_output(desicion_schema)

def supervisor_agent(state : analyst_state):
    messages = state['messages']
    response = supervisor_llm.invoke([SystemMessage(sys_prompt)] + messages)
    return {"next" : f"{response.next}"}