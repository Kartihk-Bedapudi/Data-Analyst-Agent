from agents.executer_agent import sql_agent
from agents.supervisor_agent import supervisor_agent
from agents.visualizer_agent import visualize_agent
from state import analyst_state
from tools.sql_tools.query_executer import query_executer_tool
from typing import TypedDict
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import MessagesState
from IPython.display import display,Image

def route_desicion(state : analyst_state):
    next = state['next']
    if next.lower() == "finish":
        return END
    return next

builder = StateGraph(analyst_state)

builder.add_node("supervisor_agent" , supervisor_agent)
builder.add_node("sql_agent" , sql_agent)
builder.add_node("visualize_agent",visualize_agent)
builder.add_node("tools",ToolNode(query_executer_tool))

builder.add_edge(START,"supervisor_agent")
builder.add_conditional_edges("supervisor_agent",route_desicion,["sql_agent","visualize_agent",END])
builder.add_conditional_edges("sql_agent",tools_condition,{"tools" : "tools","__end__" : "supervisor_agent"})
builder.add_edge("tools","sql_agent")
builder.add_edge("visualize_agent","supervisor_agent")
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
graph = builder.compile(checkpointer = memory)

config = {"configurable" : {"thread_id" : "000108"}}

def main():
    while True:
        try:
            humn_msg = input("user :")
            for event in graph.stream({"messages" : [HumanMessage(humn_msg)]},config,stream_mode="values"):
                event["messages"][-1].pretty_print()
        except KeyboardInterrupt as e:
            break
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()