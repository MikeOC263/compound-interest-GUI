# Helps create a DataFrame from the database
import pandas as pd
# GUI Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
# Convert the "pandas.tslib.Timestamp" --> into a "datetime" object
# For the purpose of extracting the DATE, without the TIMESTAMP
import datetime


# ____________________________CREATING DATAFRAME FROM CSV TO ENSURE WE CAN MANIPULATE THE DATA IN THE DATABASE______________________

df = pd.read_excel(
    '/Users/michaeloconnor/Desktop/python_credit_card.xlsx').fillna(0)


# _______________________________________CALCULATIONS FOR THE DATAFRAME COLUMNS_________________________________________________________

df['DEBIT (£)'] = df['DEBIT (£)'].round(decimals=2)

df['CREDIT (£)'] = df['CREDIT (£)'].round(decimals=2)

df['BALANCE (£)'] = (df['DEBIT (£)'].cumsum() +
                     df['CREDIT (£)'].cumsum()).round(decimals=2)

df['INTEREST ACCRUED (£)'] = round(-1 * df['BALANCE (£)'] *
                                   df['DAILY INTEREST (%)'] * (1/100), 2)

df['TRANSACTION DATE'] = pd.to_datetime(
    df['TRANSACTION DATE']).apply(lambda x: x.date())


# ^(Ensures that the program doesnt print the included Timestamp)
# ^(You use the Lambda function on 'x' so that the 'x' gets returned as 'x.date()')


# _______________________CREATING A HIGH-LEVEL "TK" OBJECT - ACTS AS THE MAIN WINDOW FOR THE APPLICATION________________________

# CREATES 'TKINTER' WINDOW/ "ROOT" WINDOW
guiWindow = Tk()


# THE FRAME WIDGET - ORGANISES OTHER WIDGETS IN A USER-FRIENDLY WAY.
frameWidget = Frame(guiWindow)

# THE ACTION OF PLACING THE "FRAME" WIDGET INTO BLOCKS - BEFORE INSERTING INTO THE MAIN WINDOW
# frameWidget.pack(side=tk.BOTTOM, padx=50, pady=50)
frameWidget.place(x=20, y=200, width=1100, height=700)

# THE WIDGET USED TO DISPLAY ITEMS WITH A HIERACHY
tv = ttk.Treeview(frameWidget, columns=(1, 2, 3, 4, 5),
                  show="headings", height="32")

# THE ACTION OF PLACING THE "TREEVIEW" WIDGET INTO BLOCKS - BEFORE INSERTING INTO THE MAIN WINDOW
# (MORE SO FOR THE UPDATING OF THE TABLE....)
# tv.place(x=50, y=200, width=100, height=100)
tv.pack()

# THE ACTION OF CENTERING THE COLUMNS ON DISPLAY, WITHIN THE GUI
tv.column(1, anchor=tk.CENTER)
tv.column(2, anchor=tk.CENTER)
tv.column(3, anchor=tk.CENTER)
tv.column(4, anchor=tk.CENTER)
tv.column(5, anchor=tk.CENTER)

# LINKS THE "EXCEL TITLE COLUMNS" WITH THE GUI'S COLUMNS THAT ARE ON DISPLAY
tv.heading(1, text="DATE")
tv.heading(2, text="DEBIT (£)")
tv.heading(3, text="CREDIT (£)")
tv.heading(4, text='BALANCE (£)')
tv.heading(5, text="INTEREST ACCRUED (£)")

# ___________ CALLABLE FUNCTIONS, LINKS TO THE "BUTTON" WIDGET, DRIVES THE GUI'S "ACCOUNTING PERIOD", ON THE DISPLAY WINDOW______________

# CALLABLE FUNTION - ALLOWS THE "BUTTON" WIDGET TO CHANGE THE DATA IN THE DISPLAY WINDOW


def sheet_picker():
    # (1.1) THE LABEL FOR "CURRENT TABLE" SELECTED
    title_myLabel = Label(guiWindow, text="CURRENT TABLE SELECTED:").place(
        x=280, y=45, width=200, height=30)

    # (1.2) "DATE" INPUTTED VALUE
    date_myLabel = Label(guiWindow, text=clicked.get()).place(
        x=280, y=65, width=200, height=30)

    # (2.1) DELETING THE OLD ENTRIES FROM THE TABLE
    for i in tv.get_children():
        tv.delete(i)

    # (3.1) READING THE DATABASE FOR THE NEW ENTRIES
    df = pd.read_excel(
        '/Users/michaeloconnor/Desktop/python_credit_card.xlsx', clicked.get()).fillna(0)

    # (3.2) SETTING UP FORMULA'S FOR THE TABLE'S NEW COLUMN ENTRIES
    df['DEBIT (£)'] = df['DEBIT (£)'].round(decimals=2)
    df['CREDIT (£)'] = df['CREDIT (£)'].round(decimals=2)
    df['BALANCE (£)'] = df['DEBIT (£)'].cumsum() + df['CREDIT (£)'].cumsum()
    df['BALANCE (£)'] = df['BALANCE (£)'].round(decimals=2)
    df['INTEREST ACCRUED (£)'] = round(-1 * df['BALANCE (£)']
                                       * df['DAILY INTEREST (%)'] * (1/100), 2)
    df['TRANSACTION DATE'] = pd.to_datetime(
        df['TRANSACTION DATE']).apply(lambda x: x.date())

    # (4.1) ITTERATING THE TABLE ROWS AND INSERTING THE NEW ENTRIES
    for index, row in df.iterrows():
        tv.insert('', 'end', values=[row['TRANSACTION DATE'], row['DEBIT (£)'],
                                     row['CREDIT (£)'], row['BALANCE (£)'], row['INTEREST ACCRUED (£)']])


def row_picker():
    # (1.1) THE LABEL FOR "LAST TRANSACTION ADDED"
    title_myLabel = Label(guiWindow, text="LAST TRANSACTION ADDED:").place(
        x=705, y=50, width=200, height=20)

    # (1.2) FORMATTED STRINGS INPUTTING THE MOST RECENT TRANSACTION
    transactions_myLabel = Label(guiWindow, text=f"""DATE: {date_entry_variable.get()},
    DEBIT: {debit_entry_variable.get()},
    CREDIT: {credit_entry_variable.get()}.""").place(
        x=705, y=65, width=200, height=90)

    # # (2.1) DELETING THE OLD ENTRIES FROM THE TABLE ******
    for i in tv.get_children():
        tv.delete(i)

    # # (3.1) READING THE DATABASE FOR THE NEW ENTRIES
    df = pd.read_excel(
        '/Users/michaeloconnor/Desktop/python_credit_card.xlsx', clicked.get()).fillna(0)

    # # (3.2) SETTING UP FORMULA'S FOR THE TABLE'S NEW COLUMN ENTRIES
    df['DEBIT (£)'] = df['DEBIT (£)'].round(decimals=2)
    df['CREDIT (£)'] = df['CREDIT (£)'].round(decimals=2)
    df['BALANCE (£)'] = df['DEBIT (£)'].cumsum() + df['CREDIT (£)'].cumsum()
    df['BALANCE (£)'] = df['BALANCE (£)'].round(decimals=2)
    df['INTEREST ACCRUED (£)'] = round(-1 * df['BALANCE (£)']
                                       * df['DAILY INTEREST (%)'] * (1/100), 2)
    df['TRANSACTION DATE'] = pd.to_datetime(
        df['TRANSACTION DATE']).apply(lambda x: x.date())

    # (4.1) ITTERATING THE TABLE ROWS AND INSERTING THE NEW ENTRIES
    # [Setting the param's]

    txn_dates = df['TRANSACTION DATE']
    txn_debits = df['DEBIT (£)']
    txn_credits = df['CREDIT (£)']

    # desired_date = pd.to_datetime(date_entry_variable.get())
    desired_date = pd.to_datetime(date_entry_variable.get())

    # [The actual function...]
    data_dict = df.to_dict('dict')
    for index, date in txn_dates.items():
        if date == desired_date:
            # ___________________________________________________________________________

            new_debit_amount = txn_debits[index] + \
                float(debit_entry_variable.get())

            new_credit_amount = txn_credits[index] + \
                float(credit_entry_variable.get())

            data_dict['DEBIT (£)'][index] = new_debit_amount

            data_dict['CREDIT (£)'][index] = new_credit_amount

            df = df.from_dict(data_dict)

            df['BALANCE (£)'] = df['DEBIT (£)'].cumsum() + \
                df['CREDIT (£)'].cumsum()

            df['BALANCE (£)'] = df['BALANCE (£)'].round(decimals=2)

            df['INTEREST ACCRUED (£)'] = round(-1 * df['BALANCE (£)']
                                               * df['DAILY INTEREST (%)'] * (1/100), 2)
            print(df)

            # ___________________________________________________________________________

        else:
            pass
        # # (2.1) DELETING THE OLD ENTRIES FROM THE TABLE ******
        for i in tv.get_children():
            tv.delete(i)
        # # (2.1) ADDING THE NEW ENTRIES TO THE TABLE ******
        for index, row in df.iterrows():
            tv.insert('', 'end', values=[row['TRANSACTION DATE'], row['DEBIT (£)'],
                                         row['CREDIT (£)'], row['BALANCE (£)'], row['INTEREST ACCRUED (£)']])


# ________________________________________THE OPTIONS FROM THE "DROPDOWN-MENU" WIDGET:____________________________________________________

dropdown_options = ["2019 | 08JAN - 07FEB",
                    "2019 | 08FEB - 07MAR",
                    "2019 | 08MAR - 07APR",
                    "2019 | 08APR - 07MAY",
                    "2019 | 08MAY - 09JUN",
                    "2019 | 10JUN - 07JUL",
                    "2019 | 08JUL - 07AUG",
                    "2019 | 08AUG - 08SEP",
                    "2019 | 09SEP - 07OCT",
                    "2019 | 08OCT - 07NOV",
                    "2019 | 08NOV - 08DEC",
                    "2019 | 09DEC - 07JAN",
                    "2020 | 08JAN - 09FEB",
                    "2020 | 10FEB - 08MAR",
                    "2020 | 09MAR - 07APR",
                    "2020 | 08APR - 07MAY",
                    "2020 | 08MAY - 07JUN"]


# __________________________________________THE OPTIONS FROM THE "DROPDOWN-MENU" WIDGET:____________________________________________________

# HELPS RECOGNISE THE SELECTED OPTION FOR THE "DROPDOWN-MENU" WIDGET, WHEN USING "clicked.set()"
clicked = StringVar()

# BY USING 'dropdown_options[0]' means that the prompted date on the DROPDOWN is the first from the 'dropdown_options' List
clicked.set(dropdown_options[0])


#  "clicked" ASSIGNS A STRING VARIABLE, SO THAT WHAT EVER ITEM WE SELECT FROM THE DROPDOWN
#  THAT SAME ITEM THEN GETS ASSIGNED AS A VARIABLE (A STRING VARAIBLE).
drop = OptionMenu(guiWindow, clicked, *dropdown_options)
drop.place(x=60, y=15, width=200, height=30)
# drop.pack(side=tk.LEFT, padx=5, pady=10)

# THE "BUTTON" WIDGET, WHICH LINKS TO THE "CALLABLE FUNCTION"
# (WHICH IN TURN DRIVES WHAT DATA IS DISPLAYED ON THE GUI)
dropdown_button = Button(
    guiWindow, text="UPDATE TABLE...", command=sheet_picker).place(x=280, y=15, width=200, height=30)
# pack(side=tk.LEFT)


# POPULATING THE GUI VIA THE DATABASE
for index, row in df.iterrows():
    tv.insert('', 'end', values=[row['TRANSACTION DATE'], row['DEBIT (£)'],
                                 row['CREDIT (£)'], row['BALANCE (£)'], row['INTEREST ACCRUED (£)']])

# __________________( 1ofXXTEMPT TURN OFF 1825 10062020) UPDATING TRANSACTIONS (DEBIT & CREDIT), VIA DATE ENTRY______________________

# THE "DATE" TITLE
Label(guiWindow, text="DATE:").place(x=480, y=15, width=100, height=38)

# THE "DEBIT" TITLE
Label(guiWindow, text="DEBIT:").place(x=480, y=45, width=100, height=38)

# THE "CREDIT" TITLE
Label(guiWindow, text="CREDIT:").place(x=480, y=75, width=100, height=38)

# THE "DATE" INPUT BOX
date_entry_variable = StringVar()
date_entry = tk.Entry(
    guiWindow, textvariable=date_entry_variable, width=10)
date_entry_variable.set("2020-02-28")
date_entry.place(x=565, y=15, width=100, height=30)

# THE "DEBIT" INPUT BOX
debit_entry_variable = StringVar()
debit_entry = tk.Entry(
    guiWindow, textvariable=debit_entry_variable, width=10)
debit_entry_variable.set("-9.99")
debit_entry.place(x=565, y=45, width=100, height=30)

# THE "CREDIT" INPUT BOX
credit_entry_variable = StringVar()
credit_entry = tk.Entry(
    guiWindow, textvariable=credit_entry_variable, width=10)
credit_entry_variable.set("20.00")
credit_entry.place(x=565, y=75, width=100, height=30)
# **************
# THE "ADD TRANSACTION" BUTTON
add_transaction_button = Button(
    guiWindow, text="ADD TRANSACTION...", command=row_picker).place(x=685, y=15, width=238, height=30)
# , command=


# ________________________________________________MAIN PROGRAM WINDOW PROPERTIES_________________________________________________________

# THE TITLE OF THE MAIN PROGRAM
guiWindow.title("CREDIT CARD PROGRAM")

# THE DIMENSIONS FOR THE WINDOW, IN THE MAIN PROGRAM
guiWindow.geometry("1150x850")


# ALLOWS THE MAIN PROGRAM WINDOW (TKINTER/ROOT WINDOW) TO CHANGE IT'S SIZE ACCORDING TO THE USERS NEEDS
# guiWindow.resizable(height = False, width = None)
guiWindow.resizable(height=False, width=False)


# THE METHOD ON THE MAIN WINDOW WHICH WE EXECUTE WHEN WE WANT TO RUN OUR MAIN PROGRAM
# This method will loop forever, waiting for events from the user...
# Until the user exits the program – either by closing the window, or by terminating the program with a keyboard interrupt in the console.
guiWindow.mainloop()


# __________________________________THE PROGRAM THAT WRITES ONTO THE PHYSICAL EXCEL DATABASE_______________________________________________

# writer = pd.ExcelWriter(
#     '/Users/michaeloconnor/Desktop/new_book.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='Sheet1')
# writer.save()
# print("EXCEL SHEET CREATED")
