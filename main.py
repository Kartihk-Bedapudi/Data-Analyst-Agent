from file_uploader import upload_file
import os
import duckdb
import pandas as pd

print("upload the file that need to analyse")
# file_path = upload_file()
file_path = "C:/Users/karth/Downloads/fifa_world_cup_2026_player_performance.csv"
file_type = os.path.splitext(file_path)[-1]


conn = duckdb.connect()

if file_type == ".csv":
    df = pd.read_csv(file_path)
if file_type == ".xlsx":
    df = pd.read_excel(file_path)

for col in df.select_dtypes(include = ['str']):
    df[col] = df[col].astype(str).replace({r'"' : ""},regex = True)
for col in df.columns:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col],errors = 'coerce')

conn.register("uploaded_data",df)

schema = "Table_Name : uploaded_data\ncolumns :\n"
discription = conn.execute("DESCRIBE uploaded_data").fetchall()
for col in discription:
    schema = schema + f"   - {col[0]} ({col[1]})\n"

from langchain.chat_models import init_chat_model
from typing import TypedDict
from langchain.messages import HumanMessage,SystemMessage
from langgraph.graph import MessagesState
llm = init_chat_model("groq:openai/gpt-oss-120b")


from langgraph.graph import StateGraph,START,END

from langchain.tools import tool

@tool
def query_executer(queries : list[str]) -> str:
    """
    execute the sql queries and returns the output
    
    Args : 
        qurries : list,(description: sql query)
    """
    response = ""
    for query in queries:
        try:
            response = response + f"{conn.execute(query).df()}\n"
        except Exception as e:
            response = response + f"QUERY: {query} \n ERROR: {e}"
    return response
tools = [query_executer]
llm_with_tools = llm.bind_tools(tools)

sys_prompt = """You are an expert in writing sql queries, you job is to change the user given 
                natural language query into an list of error less SQL QUERIES or a single QUERY in a list.
                here is the schema of the table you are dealing with 
                SCHEMA: {schema}
                
                INSTRUCTIONS : 
                1. you are allowed to use tools to complete user task.
                2. once you get response from a tool call write the response in a professional natural language to the user.
                """
                

class analyst_state(MessagesState):
    pass

def sql_agent(state : analyst_state):
    sys_msg = sys_prompt.replace("{schema}",schema)
    response = llm_with_tools.invoke([SystemMessage(sys_msg)]+ state["messages"])
    return {"messages" : [response]}



from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import MessagesState

builder = StateGraph(analyst_state)

builder.add_node("agent" , sql_agent)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"agent")
builder.add_conditional_edges("agent",tools_condition)
builder.add_edge("tools","agent")
builder.add_edge("agent",END)

from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
graph = builder.compile(checkpointer = memory)

config = {"configurable" : {"thread_id" : "2"}}

#####testing
messages = graph.invoke({"messages" : [HumanMessage("who is most aged player?")]},config)
for m in messages["messages"]:
    m.pretty_print()
    
messages = graph.invoke({"messages" : [HumanMessage("now tell me his nationality and how many goals he shot")]},config)
for m in messages["messages"]:
    m.pretty_print()