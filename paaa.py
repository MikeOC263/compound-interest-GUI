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
        # ALLOWING US TO PRODUCE THE LAST "formatted_period" -- "2020 | 08JUN - 07 JUL"
        start_period = sorted_start_dates[index]
        end_period = sorted_start_dates[index] + timedelta(days=29)
        defined_periods.append([start_period, end_period])
        whole_period = start_period.strftime(
            '%Y') + " " + "|" + " " + start_period.strftime('%d%b') + " - " + end_period.strftime('%d%b')
        whole_period = whole_period.upper()
        formatted_periods.append(whole_period)
        

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
    # DELETING OLD ENTRIES FROM THE TABLE
    for i in tv.get_children():
        tv.delete(i)
    # THE LABEL FOR "LAST TRANSACTION ADDED"
    titleMyLabel = Label(guiWindow, text="LAST TRANSACTION ADDED: ").place(
        x=705, y=50, width=200, height=20)
    # FORMATTED STRINGS FOR INPUTTING THE MOST RECENT TRANSACTIONS
    transactionsMyLabel = Label(guiWindow, text=f"""DATE: {date_entry_variable.get()},
    DEBIT: {debit_entry_variable.get()},
    CREDIT: {credit_entry_variable.get()}""").place(x=705, y=65, width=200, height=90)
    # READING THE DATABASE FOR THE NEW ENTRIES
    dfRow = pd.read_excel(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)
    # SETTING UP THE NEW DATAFRAM COLUMNS
    dfRow['DATE'] = pd.to_datetime(dfRow['DATE']).apply(lambda x: x.date())
    dfRow['DEBIT'] = dfRow['DEBIT'].round(decimals=2)
    dfRow['CREDIT'] = dfRow['CREDIT'].round(decimals=2)
    periods = []
    for row in dfRow['DATE']:
        #
        start1 = datetime.datetime.strptime('2019-01-08', '%Y-%m-%d').date()
        end1 = datetime.datetime.strptime('2019-02-07', '%Y-%m-%d').date()
        period1 = "2019 | 08JAN - 07FEB"
        #
        start2 = datetime.datetime.strptime('2019-02-08', '%Y-%m-%d').date()
        end2 = datetime.datetime.strptime('2019-03-07', '%Y-%m-%d').date()
        period2 = "2019 | 08FEB - 07MAR"
        #
        start3 = datetime.datetime.strptime('2019-03-08', '%Y-%m-%d').date()
        end3 = datetime.datetime.strptime('2019-04-07', '%Y-%m-%d').date()
        period3 = "2019 | 08MAR - 07APR"
        #
        start4 = datetime.datetime.strptime('2019-04-08', '%Y-%m-%d').date()
        end4 = datetime.datetime.strptime('2019-05-07', '%Y-%m-%d').date()
        period4 = "2019 | 08APR - 07MAY"
        #
        start5 = datetime.datetime.strptime('2019-05-08', '%Y-%m-%d').date()
        end5 = datetime.datetime.strptime('2019-06-09', '%Y-%m-%d').date()
        period5 = "2019 | 08MAY - 09JUN"
        #
        start6 = datetime.datetime.strptime('2019-06-10', '%Y-%m-%d').date()
        end6 = datetime.datetime.strptime('2019-07-07', '%Y-%m-%d').date()
        period6 = "2019 | 10JUN - 07JUL"
        #
        start7 = datetime.datetime.strptime('2019-07-08', '%Y-%m-%d').date()
        end7 = datetime.datetime.strptime('2019-08-07', '%Y-%m-%d').date()
        period7 = "2019 | 08JUL - 07AUG"
        #
        start8 = datetime.datetime.strptime('2019-08-08', '%Y-%m-%d').date()
        end8 = datetime.datetime.strptime('2019-09-08', '%Y-%m-%d').date()
        period8 = "2019 | 08AUG - 08SEP"
        #
        start9 = datetime.datetime.strptime('2019-09-09', '%Y-%m-%d').date()
        end9 = datetime.datetime.strptime('2019-10-07', '%Y-%m-%d').date()
        period9 = "2019 | 09SEP - 07OCT"
        #
        start10 = datetime.datetime.strptime('2019-10-08', '%Y-%m-%d').date()
        end10 = datetime.datetime.strptime('2019-11-07', '%Y-%m-%d').date()
        period10 = "2019 | 08OCT - 07NOV"
        #
        start11 = datetime.datetime.strptime('2019-11-08', '%Y-%m-%d').date()
        end11 = datetime.datetime.strptime('2019-12-08', '%Y-%m-%d').date()
        period11 = "2019 | 08NOV - 08DEC"
        #
        start12 = datetime.datetime.strptime('2019-12-09', '%Y-%m-%d').date()
        end12 = datetime.datetime.strptime('2020-01-07', '%Y-%m-%d').date()
        period12 = "2019 | 09DEC - 07JAN"
        #
        start13 = datetime.datetime.strptime('2020-01-08', '%Y-%m-%d').date()
        end13 = datetime.datetime.strptime('2020-02-09', '%Y-%m-%d').date()
        period13 = "2020 | 08JAN - 09FEB"
        #
        start14 = datetime.datetime.strptime('2020-02-10', '%Y-%m-%d').date()
        end14 = datetime.datetime.strptime('2020-03-08', '%Y-%m-%d').date()
        period14 = "2020 | 10FEB - 08MAR"
        #
        start15 = datetime.datetime.strptime('2020-03-09', '%Y-%m-%d').date()
        end15 = datetime.datetime.strptime('2020-04-07', '%Y-%m-%d').date()
        period15 = "2020 | 09MAR - 07APR"
        #
        start16 = datetime.datetime.strptime('2020-04-08', '%Y-%m-%d').date()
        end16 = datetime.datetime.strptime('2020-05-07', '%Y-%m-%d').date()
        period16 = "2020 | 08APR - 07MAY"
        #
        start17 = datetime.datetime.strptime('2020-05-08', '%Y-%m-%d').date()
        end17 = datetime.datetime.strptime('2019-06-07', '%Y-%m-%d').date()
        period17 = "2020 | 08MAY - 07JUN"
        #
        start18 = datetime.datetime.strptime('2020-06-08', '%Y-%m-%d').date()
        end18 = datetime.datetime.strptime('2020-07-07', '%Y-%m-%d').date()
        period18 = "2020 | 08JUN - 07JUL"
        #
        if (row >= start1) & (row <= end1):
            periods.append(period1)
        elif (row >= start2) & (row <= end2):
            periods.append(period2)
        elif (row >= start3) & (row <= end3):
            periods.append(period3)
        elif (row >= start4) & (row <= end4):
            periods.append(period4)
        elif (row >= start5) & (row <= end5):
            periods.append(period5)
        elif (row >= start6) & (row <= end6):
            periods.append(period6)
        elif (row >= start7) & (row <= end7):
            periods.append(period7)
        elif (row >= start8) & (row <= end8):
            periods.append(period8)
        elif (row >= start9) & (row <= end9):
            periods.append(period9)
        elif (row >= start10) & (row <= end10):
            periods.append(period10)
        elif (row >= start11) & (row <= end11):
            periods.append(period11)
        elif (row >= start12) & (row <= end12):
            periods.append(period12)
        elif (row >= start13) & (row <= end13):
            periods.append(period13)
        elif (row >= start14) & (row <= end14):
            periods.append(period14)
        elif (row >= start15) & (row <= end15):
            periods.append(period15)
        elif (row >= start16) & (row <= end16):
            periods.append(period16)
            # FILLING IN THE LAST PERIOD (HACKY ALTERNATIVE)
        elif (row >= start18) & (row <= end18):
            periods.append(period18)
            # FILLING IN THE SECOND TO LAST PERIOD - NOW THAT ALL OTHER PERIODS HAVE BEEN FILLED (HACKY ALTERNATIVE)
        else:
            periods.append(period17)
    dfRow['PERIOD'] = periods
    
    # CHANGE "date_entry_variable.get()" FROM A 'STRING' -> 'DATETIME.DATE' CLASS
    # FOR THE PURPOSE OF GETTING THE CORRESPONDING PERIOD - TO THE INPUTTED DATE
    dateEntry = datetime.datetime.strptime(
        date_entry_variable.get(), "%Y-%m-%d").date()
    
    # THE CURRENT CORRESPONDNING PERIOD - FOR THE NEWLY ADDED TRANSACTION
    periodEntry = dfRow.loc[dfRow['DATE'] == dateEntry, 'PERIOD'].values[0]
    
    # CREATING INDEXES FOR EACH "formatted_period", TO BE USED LATER ON FOR COMPARISONS
    idx_formatted_periods = []
    for i in range(len(formatted_periods)):
        idx_formatted_periods.append(i)
        
    # STORING 'formatted_periods' WITH 'indexes' INTO A DICTIONARY (periodDict)
    periodDict = dict(zip(formatted_periods, idx_formatted_periods))
    
    # CREATING A DICTIONARY FOR NEWLY ADDED TRANSACTION (including all relevant details)
    txnDict = dict(date=dateEntry, debit=debit_entry_variable.get(),
                   credit=credit_entry_variable.get(), period=periodEntry)
    
    # SETTING THE PARAMETERS
    txnDates = dfRow['DATE']
    txnDebits = dfRow['DEBIT']
    txnCredits = dfRow['CREDIT']
    txnPeriod = dfRow['PERIOD']
    desiredDate = datetime.datetime.strptime(date_entry_variable.get(), "%Y-%m-%d").date()
    
    # STORE THE INDEX, RELATING TO THE 'PERIOD' FOR THE NEWLY ADDED TRANSACTION
    # FOR THE FINAL PURPOSE OF INCLUDING THIS TRANSACTION TO ALL 'higher' PERIODS (for the beggining date in that period)
    # (Key= formatted_period), (Value= idx_formatted_period)
    firstPeriods = []
    for key, value in periodDict.items():
        firstPeriods = []
        if key == periodEntry:
            periodNo = value
        else:
            pass
    for key, value in periodDict.items():
        if value > periodNo:
            firstPeriods.append(key)
        else:
            pass
    
    # EXTRACTING THE CORRESPONDING "PERIOD"
    for index, date in txnDates.items():
        if date == desiredDate:
            periodMask = dfRow['PERIOD'][index]
            print(dfRow['PERIOD'][index])
        else:
            pass      
        
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
            # FILTERING THE DATAFRAME BASED ON THE 'PERIOD' OF THE INPUTTED DATE
            filterMask = (dfRow['PERIOD'] == periodMask)
            dfRow = dfRow[filterMask]

        else:
            pass
        
    # FOR LOADING THE FILE INTO "book"
    book = load_workbook(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx')
    # CREATES A PANDAS EXCEL WRITER BY USING AN "opnpyxl" ENGINE ONTO THE "INITIAL DATABASE"
    writer = pd.ExcelWriter(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx', engine='openpyxl')
    # SETTING THE "writer.book" VALUE TO BE "book"
    writer.book = book
    # CREATES A DICTIONARY OF KEY/VALUE PAIRS - {'sheet_titles' : sheet}
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    # CONVERTS THE "DATAFRAME" OBJECT INTO AN "XLSX WRITER" OBJECT
    dfRow.to_excel(writer, sheet_name='Sheet1', index=False)
    # CLOSING THE PANDAS "XLSX WRITER" AND OUTPUTTING THE EXCEL FILE
    writer.save()    
    # INSERT THE NEWLY UPDATED DATAFRAME VALUES INTO THE TKK.TREEVIEW WIDGET
    print(dfRow)
    for index, row in dfRow.iterrows():
        tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT']])
        


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
