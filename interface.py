import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st 
import csv

root = tk.Tk()

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/aaronhampson/Downloads/ASDYHUSAJDB/murder-mystery.db')
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Get a list of table names in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()
table_names = [table[0] for table in table_names] 

# Read each table into a separate DataFrame
dataframes = {}
for table_name in table_names:
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        dataframes[table_name] = df
    except Exception as e:
        print(f"Error reading table {table_name}: {str(e)}")

# Close the database connection
conn.close()
buttons = []

def display_csv(choice):
    # Create the main window.
    secondary_window = tk.Toplevel()
    secondary_window.title(choice)
    secondary_window.config(width=800, height=800)

    # Create a Treeview widget.
    text_area = st.ScrolledText(secondary_window, width=70, height=70)
    text_area.grid(column=0, pady=10, padx=10)

    text_area.insert(tk.INSERT, dataframes[choice])
    text_area.configure(state ='disabled') 


for i in dataframes:
    cur = tk.Button(root, text=f"{str(i)}", command = lambda i=i: display_csv(i))
    buttons.append(cur)

for i in buttons:
    i.pack()

root.mainloop()