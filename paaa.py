import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
import datetime
from datetime import timedelta

# READING THE DATABASE FOR OUR RAW DATA SET
df = pd.read_excel(
    '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx', nrows=31).fillna(0)
# PREPPING DATAFRAME COLUMNS
df['DATE'] = pd.to_datetime(df['DATE']).apply(lambda x: x.date())
df['DEBIT'] = df['DEBIT'].round(decimals=2)
df['CREDIT'] = df['CREDIT'].round(decimals=2)

# ________________________________________________________________________________________________________
# USING SEPERATE DATAFRAME TO EXTRACT DATES
dfDates = pd.read_excel(
    '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)
# FORMATTING THE DATES IN THE NEW DATAFRAME
dfDates['DATE'] = pd.to_datetime(dfDates['DATE']).apply(lambda x: x.date())
# THE 8th OF ALL MONTHS
start_dates = []
txn_dates = dfDates['DATE']
for index, date in txn_dates.items():
    if date.day == 8:
        start_dates.append(date)
    else:
        pass

# WHEN 8th OCCURS ON A SATURDAY
for date in start_dates:
    if date.weekday() == 5:
        new_start_date = date + timedelta(days=2)
        start_dates.remove(date)
        start_dates.append(new_start_date)
        # print("date.weekday() == 5", date)
        # print("new_start_date", new_start_date)

# WHEN 8th OCCURS ON A SUNDAY
for date in start_dates:
    if date.weekday() == 6:
        new_start_date = date + timedelta(days=1)
        start_dates.remove(date)
        start_dates.append(new_start_date)
        # print("date.weekday() == 6", date)
        # print("new_start_date", new_start_date)

# SORTING IN ORDER THE NEWLY ADJUSTED DAYS (anything but the 8th)
sorted_start_dates = sorted(start_dates)

# SETTING UP DATE DATE PAIRS - PER PERIOD
period_dates = enumerate(sorted_start_dates)
number_of_elements = len(sorted_start_dates)
index_of_last_element = number_of_elements - 1
formatted_periods = []
defined_periods = []
for index, date in period_dates:
    if index != index_of_last_element:
        start_period = sorted_start_dates[index]
        end_period = sorted_start_dates[(
            index + 1)] - timedelta(days=1)
        defined_periods.append([start_period, end_period])
        whole_period = start_period.strftime(
            '%Y') + " " + "|" + " " + start_period.strftime('%d%b') + " - " + end_period.strftime('%d%b')
        whole_period = whole_period.upper()
        formatted_periods.append(whole_period)
    else:
        pass

dictionary = dict(zip(formatted_periods, defined_periods))


# ________________________________________________________________________________________________________________

# print(df)

# ________________________________________________________________________________________________________________

# CREATES THE MAIN WINDOW OF THE APPLICATION
guiWindow = Tk()
# THE TITLE OF THE MAIN PROGRAM
guiWindow.title("CREDIT CARD PROGRAM")
# THE DIMENSIONS FOR THE WINDOW, IN THE MAIN PROGRAM
guiWindow.geometry("1150x850")
# ENUSRES THE MAIN WINDOW FOR THE APPPLICATION ISN'T RESIZABLE
guiWindow.resizable(height=False, width=False)


# A CONTAINER WIDGET IN THE MAIN WINDOW
frameWidget = Frame(guiWindow)
# POSITIONING OF THE CONTAINER WIDGET
frameWidget.place(x=20, y=200, width=1100, height=700)


# FUNCTION TO CHANGE THE TABLES DISPLAYED MONTH
def sheetPicker():
    # "CURRENT TABLE SELECTED" LABEL
    tableSelectedLabel = Label(guiWindow, text="CURRENT TABLE SELECTED").place(
        x=280, y=45, width=200, height=30)
    # CORRESPONDING "DATE" FOR TABLE
    dateSelectedLabel = Label(guiWindow, text=clicked.get()).place(
        x=280, y=65, width=200, height=30)
    # DELETING THE OLD TABLE DATA
    for i in tv.get_children():
        tv.delete(i)

    # CREATING A NEW DATAFRAME TO EXTRACT FROM
    dfTable = pd.read_excel(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)
    # SETTING UP THE NEW DATAFRAME COLUMNS
    dfTable['DATE'] = pd.to_datetime(dfTable['DATE']).apply(lambda x: x.date())
    dfTable['DEBIT'] = dfTable['DEBIT'].round(decimals=2)
    dfTable['CREDIT'] = dfTable['CREDIT'].round(decimals=2)
    # ITERATIONG THE TABLE ROWS

    startPeriod = dictionary[f'{clicked.get()}'][0]
    endPeriod = dictionary[f'{clicked.get()}'][1]
    period = dfTable['DATE'].between(startPeriod, endPeriod, inclusive=True)
    tableDataFrame = dfTable[period]
    for index, row in tableDataFrame.iterrows():
        tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT']])

# FUNCTION TO ADD NEW TRANSACTIONS INTO THE TABLE AND DATABASE


def rowPicker():
    # THE LABEL FOR "LAST TRANSACTION ADDED"
    titleMyLabel = Label(guiWindow, text="LAST TRANSACTION ADDED: ").place(
        x=705, y=50, width=200, height=20)
    # FORMATTED STRINGS FOR INPUTTING THE MOST RECENT TRANSACTIONS
    transactionsMyLabel = Label(guiWindow, text=f"""DATE: {date_entry_variable.get()},
    DEBIT: {debit_entry_variable.get()},
    CREDIT: {credit_entry_variable.get()}""").place(x=705, y=65, width=200, height=90)
    # DELETING OLD ENTRIES FROM THE TABLE
    for i in tv.get_children():
        tv.delete(i)
    # READING THE DATABASE FOR THE NEW ENTRIES
    dfRow = pd.read_excel(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)
    # SETTING UP THE NEW DATAFRAM COLUMNS
    dfRow['DATE'] = pd.to_datetime(dfRow['DATE']).apply(lambda x: x.date())
    dfRow['DEBIT'] = dfRow['DEBIT'].round(decimals=2)
    dfRow['CREDIT'] = dfRow['CREDIT'].round(decimals=2)
    # SETTING THE PARAMETERS
    txnDates = dfRow['DATE']
    txnDebits = dfRow['DEBIT']
    txnCredits = dfRow['CREDIT']
    desiredDate = datetime.datetime.strptime(date_entry_variable.get(), "%Y-%m-%d").date()
    # TURNING DATAFRAME TO DICTIONARY, SO TXN VALUES CAN BE EDITED FROM RECORDS
    dataDict = dfRow.to_dict('dict')
    for index, date in txnDates.items():
        # IF 'DATAFRAME DATE' == 'INPUTTED DATE' THEN:
        if date == desiredDate:
            # ADDS THE INPUTTED 'DEBIT' NUMBER TO THE RECORDED 'DEBIT' NUMBER IN DATABASE
            newDebitAmount = txnDebits[index] + \
                float(debit_entry_variable.get())
            # ASSIGN THE NEW NUMBER FOR THE SPECIFIC INDEX, OF THE 'DEBIT' COLUMN
            dataDict['DEBIT'][index] = newDebitAmount
            # ADDS THE INPUTTED 'CREDIT' NUMBER TO THE RECORDED 'CREDIT' NUMBER IN DATABASE
            newCreditAmount = txnCredits[index] + \
                float(credit_entry_variable.get())
            # ASSIGN THE NEW NUMBER FOR THE SPECIFIC INDEX, OF THE 'CREDIT' COLUMN
            dataDict['CREDIT'][index] = newCreditAmount
            # TURNING THE DICTIONARY BACK INTO A DATAFRAME, AS NEW TXN VALUES NEED TO BE CEMENTED IN
            dfRow = dfRow.from_dict(dataDict)

        else:
            pass

        print(dfRow)


# THE SELECTED OPTION, FROM THE DROPDOWN-MENU, GETS SET AS A STRING VARIABLE.
clicked = StringVar()
# SETS THE TEXT SHOWN ON THE BUTTON
clicked.set(formatted_periods[0])
# CREATING THE DROPDOWN-MENU
dropDownMenu = OptionMenu(guiWindow, clicked, *formatted_periods)
# POSITIONING THE DROPDOWN-MENU INSIDE THE MAIN PROGRAMS WINDOW
dropDownMenu.place(x=60, y=15, width=200, height=30)
# CREATING THE DROPDOWN BUTTON
dropDownButton = Button(guiWindow, text="UPDATE TABLE...",
                        command=sheetPicker).place(x=280, y=15, width=200, height=30)


# THE "DATE" TITLE
Label(guiWindow, text="DATE").place(x=480, y=15, width=100, height=38)
# THE "DATE" INPUT FIELD
date_entry_variable = StringVar()
date_entry = tk.Entry(guiWindow, textvariable=date_entry_variable, width=10)
date_entry_variable.set("2019-01-08")
date_entry.place(x=565, y=15, width=100, height=30)
# THE "DEBIT" TITLE
Label(guiWindow, text="DEBIT").place(x=480, y=45, width=100, height=38)
# THE "DEBIT" INPUT FIELD
debit_entry_variable = StringVar()
debit_entry = tk.Entry(guiWindow, textvariable=debit_entry_variable, width=10)
debit_entry_variable.set("-9.99")
debit_entry.place(x=565, y=45, width=100, height=30)
# THE "CREDIT" TITLE
Label(guiWindow, text="CREDIT").place(x=480, y=75, width=100, height=38)
# THE "CREDIT" INPUT FIELD
credit_entry_variable = StringVar()
credit_entry = tk.Entry(
    guiWindow, textvariable=credit_entry_variable, width=10)
credit_entry_variable.set("20.00")
credit_entry.place(x=565, y=75, width=100, height=30)
# "ADD TRANSACTION" BUTTON
add_transaction_button = Button(guiWindow, text="ADD TRANSACTION...", command=rowPicker).place(
    x=685, y=15, width=238, height=30)


# WIDGET USED TO DISPLAY ITEMS WITH A HIERACHY
tv = ttk.Treeview(frameWidget, columns=(1, 2, 3, 4, 5),
                  show="headings", height="32")
# THE ACTION OF CENTERING THE COLUMNS ON DISPLAY, WITHIN THE CONTAINER WIDGET
tv.column(1, anchor=tk.CENTER)
tv.column(2, anchor=tk.CENTER)
tv.column(3, anchor=tk.CENTER)
tv.column(4, anchor=tk.CENTER)
tv.column(5, anchor=tk.CENTER)
# LINKS THE "EXCEL TITLE COLUMNS" WITH THE GUI'S COLUMNS THAT ARE ON DISPLAY
tv.heading(1, text="DATE")
tv.heading(2, text="DEBIT")
tv.heading(3, text="CREDIT")
tv.heading(4, text="BALANCE")
tv.heading(5, text="INTEREST")
# THE ACTION OF PLACING THE "TREEVIEW" WIDGET INTO BLOCKS - BEFORE INSERTING INTO THE MAIN WINDOW
# (MORE SO FOR THE UPDATING OF THE TABLE....)
tv.pack()
# EXPORTING THE DATABASE INFO INTO THE "TREEVIEW" WIDGET (FOR DISPLAY)
for index, row in df.iterrows():
    tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT']])


# THE METHOD ON THE MAIN WINDOW WHICH WE EXECUTE WHEN WE WANT TO RUN OUR MAIN PROGRAM
# This method will loop forever, waiting for events from the user...
guiWindow.mainloop()

# ________________________________________________________________________________________________________________

# print(defined_periods)

# [datetime.date(2019, 1, 8), datetime.date(2019, 2, 7)]
# print(defined_periods[0])

# [datetime.date(2019, 1, 8)
# print(defined_periods[0][0])
