import pandas as pd
import schedule
import time
import datetime
from openpyxl import Workbook
import mysql.connector
import uuid


def update_excel():
    
    db_connection = mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="",       
        database="perusahaan"  
    )
    
    query = "SELECT * FROM t_prod"
    data_frame = pd.read_sql(query, db_connection)
    
    file_path = "data_excel.xlsx"
    try:
        data_frame.to_excel(file_path, sheet_name='Sheet1', index=False)
        print("Data updated successfully.")
    except Exception as e:
        print("An error occurred:", str(e))


def run_scheduled_updates():
    while True:
        schedule.run_pending()
        time.sleep(1)


def enter_token():
    entered_token = input("Enter your token: ")
    return entered_token


def generate_token():
    return str(uuid.uuid4())

token = generate_token()



with open("token.txt", "w") as file:
    file.write(token)


entered_token = enter_token()
if entered_token == token:
    schedule.every(4).seconds.do(update_excel)
    run_scheduled_updates()
    print("Automated updates started.")
    
    
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
    while datetime.datetime.now() < end_time:
        schedule.run_pending()
        time.sleep(1)
    
    print("Automated updates stopped after 10 seconds.")
else:
    print("Invalid token. Automated updates require a valid token.")
