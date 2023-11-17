import io
import re
import pandas as pd
from typing import TextIO
from tkinter import *
from tkinter import messagebox, filedialog
import mysql.connector


f1 = ('arial', 15, 'bold')
f2 = ('arial', 10, 'bold')
f3 = ('arial', 5, 'italic')


def chooseFile():
    global file_path
    global data

    try:
        file_path = filedialog.askopenfile(title="Select File", filetypes=[('csv files "ONLY"',"*.csv")]).name
        label2.config(text="File Location: "+file_path)
        data = pd.read_csv(file_path)
    except ValueError:
        messagebox.showinfo("CSV not selected", "Please Select A CSV FILE")
        return
    except AttributeError:
        messagebox.showinfo("CSV not selected", "Please Select A CSV FILE")
        return
    except mysql.connector.errors.ProgrammingError:
        return



def submit():
    try:
        df = pd.DataFrame(data)
        columns_len = len(df.columns)
        rows_len = len(df)
        table_name = entry1.get()
    
        if file_path == "":
            messagebox.showerror("File Path", "Please Provide File Path")
        elif table_name == "":
            messagebox.showerror("Table Name", "Please Provide A Valid Table Name")
        else:
            try:
                # Database Conncetion
                mydb = mysql.connector.connect(host='localhost', password='', user='root', database='readcsv', charset='utf8')
                mycur = mydb.cursor()
                
                # Table Creation
                create_query_string = "create table "+str(table_name)+"("
                for i in df.columns:
                    i = remove_special_symbols_and_spaces(i)
                    if df.columns[-1] == i:
                        i = ""+i+" varchar(255))"
                    else:
                        i = ""+i+" varchar(255),"
                    create_query_string += i

                mycur.execute(create_query_string)
                mydb.commit()
            
                row_index = 0
                column_index = 0

                # Data insertion into table
                insert_query_string = 'insert into '+table_name+' values('

                while rows_len > row_index:
                    while columns_len > column_index:
                        element = "'"+str(df.at[row_index, df.columns[column_index]])+"'"

                        if column_index == columns_len-1:
                            insert_query_string += element
                        else:
                            insert_query_string += element + ","
                        column_index += 1

                    column_index = 0
                    row_index += 1
                    if row_index == rows_len:
                        insert_query_string += ")"
                    else:
                        insert_query_string += "), ("

                mycur.execute(insert_query_string)
                mydb.commit()
                messagebox.showinfo("DONE", "Successful\n\t-Database Table Creation\n\t-Data Insertion\n\n"+"Table Name = "+str(table_name))
            
            except mysql.connector.errors.ProgrammingError:
                messagebox.showerror("Something Went Wrong", "Table Already Exists\nOR\nInvalid Table Name")
                return
    except NameError:
        messagebox.showerror("CSV not selected", "Please Select A CSV FILE")       



def remove_special_symbols_and_spaces(input_string):
    # Define a regex pattern to match any non-alphanumeric characters
    pattern = re.compile(r'[^a-zA-Z0-9_]')

    # Use the pattern to replace non-alphanumeric characters with an empty string
    result_string = re.sub(pattern, '', input_string)

    result_string = re.sub('_+', '_', result_string)

    return result_string



win = Tk()
win.title("Shubham Jadhav | Read .CSV and Save To Database")
win.geometry("600x300+500+222")

label1 = Label(text="Provide file location", font=f1)
label1.place(x=10, y=20)

button1 = Button(text="Choose File Location", font=f2, command=chooseFile)
button1.place(x=10, y=60)

label2 = Label(text="File Location: None", font=f2)    # label to display selected file path
label2.place(x=10, y=100)

label3 = Label(text="Create Table Name", font=f1)    # label to display "Enter table name"
label3.place(x=10, y=140)

entry1 = Entry(font=f2)             # label to enter table name
entry1.place(x=10, y=180)

button2 = Button(text="Submit", command=submit)
button2.place(x=10, y=220)

win.mainloop()
