# from file_uploader import upload_file
import os
import pandas as pd
from tools.sql_tools.file_uploader import upload_file
from connection import conn

def initiate():
    print("upload the file that need to analyse")
    file_path = upload_file()
    # file_path = "C:/Users/karth/Downloads/fifa_world_cup_2026_player_performance.csv"
    file_type = os.path.splitext(file_path)[-1]


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
    return schema,df