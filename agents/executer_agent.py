from agents.visualizer_agent import schema
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from tools.sql_tools.initial import initiate
from tools.sql_tools.query_executer import query_executer_tool
from state import analyst_state

llm = init_chat_model("groq:openai/gpt-oss-120b")
llm_with_tools = llm.bind_tools(query_executer_tool)

sys_prompt = """You are an expert in writing sql queries, you job is to change the user given 
                natural language query into an list of error less SQL QUERIES or a single QUERY in a list.
                here is the schema of the table you are dealing with 
                SCHEMA: {schema}
                
                INSTRUCTIONS : 
                1. you are allowed to use tools to complete user task.
                2. once you get response from a tool call write the response in a professional natural language to the user.
                """

def sql_agent(state : analyst_state):
    convo = state['supervisor_memory']
    sys_msg = sys_prompt.replace("{schema}",schema)
    response = llm_with_tools.invoke([SystemMessage(sys_msg)]+ state["messages"])
    return {"messages" : [response],"supervisor_memory" : f"{convo} \nsql_agent : {response.content}"}