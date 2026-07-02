from tools.sql_tools.initial import initiate
from tools.visualisation_tool import create_visualiser_tool
from state import analyst_state
from langchain.agents import create_agent
schema,df = initiate()
sys_prompt = f"""
                you are a data visualizer agent, your job is to write a python data visualisation code in seaborn,
                on the basis of user query.
            # CRITICAL :
                            CALL data_visualiser tool and send code, never give code as a chat message. only chat when the graph created successfully
                NOTE : DON'T use plt.show() in the last, just leave the code as is, don't show or save.
                
                NOTE: the code sending to the tool, MUST follow these below rules.
                
                1. you need to just write an error less python code, DONT import any thing.
                2. you are allowed to use modules -- mataploatlib.pyplot imported as plt and
                   seaborn imported as sns.
                3. and dataframe of the data imported as "my_data".
                4. and MAKE SURE TO create the graph as proffesional and understandable as possible.
                5. Passing `palette` without assigning `hue` is removed. Assign the `x` variable to `hue` and set `legend=False` for the same effect.
                    here is the schema of the data frame :
                  {schema}
"""
data_visualizer = create_visualiser_tool(df)

def visualize_agent(state : analyst_state):
    convo = state['supervisor_memory']
    data_agent = create_agent(
        model = "groq:llama-3.3-70b-versatile",
        tools = [data_visualizer],
        system_prompt = sys_prompt
    )
    response = data_agent.invoke({ "messages" : state["messages"]})
    final_response = response["messages"][-1]
    return {"messages" : [final_response],"supervisor_memory" : f"{convo} \nvisualize_agent : {final_response.content}"}