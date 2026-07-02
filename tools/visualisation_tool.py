from langchain.tools import tool
def create_visualiser_tool(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    @tool
    def data_visualizer(code : str,name : str) -> str:
        """
        this is a python code executor used to execute data visuslizing.
        
        ARGS : 
                code : str (description: python code for visualizing data)
                name : str(description: name of the graph image, name should be like a description of the graph-code. example: age_distribution_histogram)
        """
        tool_environment = {
            "plt" : plt,
            "sns" : sns,
            "my_data" : df,
            "file_name" : name
        }
        
        try:
            folder_creation = "\nfrom pathlib import Path\nsession_dir = Path('graphs/current_session')\nsession_dir.mkdir(exist_ok = True,parents = True)\n"
            silencing_warning = "import matplotlib\nmatplotlib.use('Agg')\n"
            code = folder_creation + silencing_warning + code + "\nplt.savefig(f'graphs/current_session/{file_name}.png')"
            hi = exec(code,tool_environment)
            return "code executed successfully."
        except NameError as e:
            print(f"ERROR : the following named modules are not imported\n{e}\n\n ask user to import them.")
        except Exception as e:
            print(e)
            
    return data_visualizer