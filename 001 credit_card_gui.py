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
# (NO NEED TO INCLUDE THE 'PERIOD' COLUMN, TO THE INITIAL DATAFRAME BECAUSE IT'S PURPOSE IS ONLY FOR 'CHANGING TABLE' & 'ADDING TRANSACTIONS')
df['DATE'] = pd.to_datetime(df['DATE']).apply(lambda x: x.date())
df['DEBIT'] = df['DEBIT'].round(decimals=2)
df['CREDIT'] = df['CREDIT'].round(decimals=2)
df['BALANCE'] = (df['DEBIT'].cumsum() + df['CREDIT'].cumsum()).round(decimals=2)
df['DAILY INTEREST'] = (21.87/365)
df['INTEREST'] = round(df['BALANCE'] * df['DAILY INTEREST'] * (1/100), 2)

# STORING THE 'Total Interest' INTO A VARIABLE
interestSum = df['INTEREST'].sum()

# ________________________________________________________________________________________________________

# USING SEPERATE DATAFRAME TO EXTRACT DATES
dfDates = pd.read_excel(
    '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)

# FORMATTING THE DATES IN THE NEW DATAFRAME (turns them into <class 'datetime.date'> )
dfDates['DATE'] = pd.to_datetime(dfDates['DATE']).apply(lambda x: x.date())

# GATHERING THE 8th FOR EACH MONTH
start_dates = []
txn_dates = dfDates['DATE']
for index, date in txn_dates.items():
    if date.day == 8:
        start_dates.append(date)
    else:
        pass
    
# WHEN 8th OCCURS ON A "SATURDAY" (== 5)
for date in start_dates:
    if date.weekday() == 5:
        new_start_date = date + timedelta(days=2)
        start_dates.remove(date)
        start_dates.append(new_start_date)


# WHEN 8th OCCURS ON A "SUNDAY" (== 6)
for date in start_dates:
    if date.weekday() == 6:
        new_start_date = date + timedelta(days=1)
        start_dates.remove(date)
        start_dates.append(new_start_date)


# SORTING IN ORDER THE NEWLY ADJUSTED DAYS 
# (.....HERE, THE start_dates DON'T NECESSARILT OCCUR ON THE 8TH) 
sorted_start_dates = sorted(start_dates)

# SETTING UP DATE DATE PAIRS - PER PERIOD
# period_dates - IS A NUMBERED/INDEXED VERSION OF THE start_period, FOR EACH PERIOD
# - S.T IF THIS INDEX DOESN'T MATCH THE NO. OF (INDIVIDUAL) START DATES
period_dates = enumerate(sorted_start_dates)
number_of_elements = len(sorted_start_dates)
index_of_last_element = number_of_elements - 1
formatted_periods = []
defined_periods = []
for index, date in period_dates:
    # IF THE start_period, ISN'T THE LAST ONE (CHRONOLOGICALLY), OUT OF THE LIST THEN ASSIGN ITS'...
    if index != index_of_last_element:
        # (START DATE)
        start_period = sorted_start_dates[index]
        # (END DATE)
        end_period = sorted_start_dates[(
            index + 1)] - timedelta(days=1)
        # (THEN GROUP THE ABOVE, TWO DATES INTO A "defined_period")
        defined_periods.append([start_period, end_period])
        # (AND THEN ESTABLISH THE formatted_period NAME, VIA IT'S START & END DATE)
        whole_period = start_period.strftime(
            '%Y') + " " + "|" + " " + start_period.strftime('%d%b') + " - " + end_period.strftime('%d%b')
        # (CAPITALIZE THE formatted_period)
        whole_period = whole_period.upper()
        # (THEN COLLATE THE formatted_periods INTO A LIST, TO ACCESS LATER)
        formatted_periods.append(whole_period)
    else:
        # ALLOWING US TO PRODUCE THE LAST "formatted_period" -- "2020 | 08JUN - 07 JUL"
        # (START DATE)
        start_period = sorted_start_dates[index]
        # (END DATE)
        end_period = sorted_start_dates[index] + timedelta(days=29)
        # (THEN GROUP THE ABOVE, TWO DATES INTO A "defined_period")
        defined_periods.append([start_period, end_period])
        # (AND THEN ESTABLISH THE formatted_period NAME, VIA IT'S START & END DATE)
        whole_period = start_period.strftime(
            '%Y') + " " + "|" + " " + start_period.strftime('%d%b') + " - " + end_period.strftime('%d%b')
        # (CAPITALIZE THE formatted_period)
        whole_period = whole_period.upper()
        # (THEN COLLATE THE formatted_periods INTO A LIST, TO ACCESS LATER)
        formatted_periods.append(whole_period)
        
# CREATING A DICTIONARY WITH (formatted_period,[beginning_point,end_point])
# ALLOWING YOU TO DETERMINE EACH formatted_periods's BEGINNING AND END POINT
dictionary = dict(zip(formatted_periods, defined_periods))

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
frameWidget.place(x=20, y=155, width=1100, height=700)

# ________________________________________________________________________________________________________________
# FUNCTION TO CHANGE THE TABLES DISPLAYED MONTH
def sheetPicker():
    # DELETING THE OLD TABLE DATA
    for i in tv.get_children():
        tv.delete(i)
        
    # "CURRENT TABLE SELECTED" LABEL
    tableSelectedLabel = Label(guiWindow, text="CURRENT TABLE SELECTED").place(
        x=280, y=45, width=200, height=30)
    
    # CORRESPONDING "DATE" FOR TABLE
    dateSelectedLabel = Label(guiWindow, text=clicked.get()).place(
        x=280, y=65, width=200, height=30)
    
    # CREATING A NEW DATAFRAME TO EXTRACT FROM
    dfTable = pd.read_excel(
        '/Users/michaeloconnor/Desktop/credit_card_data_set.xlsx').fillna(0)
    
    # SETTING UP THE NEW DATAFRAME COLUMNS
    dfTable['DATE'] = pd.to_datetime(dfTable['DATE']).apply(lambda x: x.date())
    dfTable['DEBIT'] = dfTable['DEBIT'].round(decimals=2)
    dfTable['CREDIT'] = dfTable['CREDIT'].round(decimals=2)
    
    # CREATING THE 'PERIOD' COLUMN, BY MAPPING THE RELEVANT 'PERIOD' FOR EACH DAY/DATE
    periods = []
    for row in dfTable['DATE']:
        for x in range(18):
            # IF THE 'row' (DATE) IS BETWEEN THE BOUNDS FOR THE 'FORMATTED PERIOD'
            # THEN INLCUDE THAT 'FORMATTED PERIOD' TO THE GIVEN DATES IN THE 'PERIOD COLUMN'                                         
            if (row >= defined_periods[x][0]) & (row <= defined_periods[x][1]):
                periods.append(formatted_periods[x])
            else:
                pass
    dfTable['PERIOD'] = periods
    
    # STORING THE START/FINISH DATE FOR THE PERIOD INTO 2 SEPERATE VARIABLES
    # dictionary[ formatted_period, [start_period, end_period] ]
    startPeriod = dictionary[f'{clicked.get()}'][0]
    endPeriod = dictionary[f'{clicked.get()}'][1]
    
    
    # CREATING A MASK TO FILTER/EXTRACT THE CORRECT DATES FOR THE RELEVANT PERIOD
    periodMask = (dfTable['DATE'] >= startPeriod) & (dfTable['DATE'] <= endPeriod)
    
    # APPLYING THE MASK TO THE DATAFRAME
    dfTable = dfTable.loc[periodMask]
    
    # AFTER APPLYING THE MASK, THE 'Daily Interest' COLUMN SEEMS TO BE DELETED (as wasn't explicitly defined before?s)
    # SO WE REAPPLY THE NUMBER MANUALLY - ONCE THE DATAFRAME HAS BEEN MODIFIED
    dfTable['DAILY INTEREST'] = (21.87/365)
    
    
    # ASSIGNING THE DATAFRAME 'BALANCE' ONCE ITS BEEN FILTERED FOR ITS PERIOD
    dfTable['BALANCE'] = (dfTable['DEBIT'].cumsum() + dfTable['CREDIT'].cumsum()).round(decimals=2)
    
    # ASSIGNING THE DATAFRAME 'INTEREST' ONCE ITS BEEN FILTERED FOR ITS PERIOD
    dfTable['INTEREST'] = round(dfTable['BALANCE'] * dfTable['DAILY INTEREST'] * (1/100), 2)
    
    # CREATING A VARIABLE TO STORE THE 'TOTAL INTEREST' FOR THAT PERIOD
    interestSum1 = (tableDataFrame['INTEREST'].sum()).round(decimals=2)
    
    # INSERTING THE DATAFRAME VALUES INTO THE TTK.TREEVIEW WIDGET-TABLE
    for index, row in tableDataFrame.iterrows():
        tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT'], row['BALANCE'], row['INTEREST']])
        
    # INSERTING THE 'Total Interest' VALUE INTO THE TTK.TREEVIEW WIDGET-TABLE
    tv.insert('', 'end', values=['', '', '', 'TOTAL INTEREST: ', interestSum1])
    
        
# ________________________________________________________________________________________________________________
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
    
    # CREATING THE 'PERIOD' COLUMN, BY MAPPING THE RELEVANT 'PERIOD' FOR EACH DAY/DATE
    periods = []
    for row in dfRow['DATE']:
        for x in range(18):
            # IF THE 'row' (DATE) IS BETWEEN THE BOUNDS FOR THE 'FORMATTED PERIOD'
            # THEN INLCUDE THAT 'FORMATTED PERIOD' TO THE GIVEN DATES IN THE 'PERIOD COLUMN'                                                                                 
            if (row >= defined_periods[x][0]) & (row <= defined_periods[x][1]):
                periods.append(formatted_periods[x])
            else:
                pass
    dfRow['PERIOD'] = periods    
    
    
    # ADD'S THE DATAFRAME BALANCE VIA (1) THE PERIOD (2) THE CUMULATIVE SUM
    dfRow['BALANCE'] = dfRow.groupby('PERIOD')['DEBIT'].transform(lambda x: x.cumsum()) + dfRow.groupby('PERIOD')['CREDIT'].transform(lambda x: x.cumsum())
    
    # "BY PERIOD" - ESTABLISHING THE AMOUNT OF INTEREST ACCRUED PER DAY/DAYS 
    dfRow['INTEREST'] = round(dfRow['BALANCE'] * dfRow['DAILY INTEREST'] * (1/100), 2)    
    
    
    # CHANGE "date_entry_variable.get()" FROM A 'STRING' -> 'DATETIME.DATE' CLASS
    # FOR THE PURPOSE OF GETTING THE CORRESPONDING PERIOD - TO THE INPUTTED DATE
    dateEntry = datetime.datetime.strptime(
        date_entry_variable.get(), "%Y-%m-%d").date()
    
    # THE CURRENT CORRESPONDNING PERIOD - FOR THE NEWLY ADDED TRANSACTION
    periodEntry = dfRow.loc[dfRow['DATE'] == dateEntry, 'PERIOD'].values[0]
    
    
    # ESTABLISHING WHAT THE TOTAL INTEREST WAS BEFORE ADDING IN A NEW TRANSACTION 
    interestSum1 = dfRow.loc[dfRow['PERIOD'] == periodEntry, 'INTEREST'].sum()    
    
    
    # CREATING INDEXES FOR EACH "formatted_period", TO BE USED LATER ON FOR COMPARISONS
    idx_formatted_periods = []
    for i in range(len(formatted_periods)):
        idx_formatted_periods.append(i)
        
    # STORING 'formatted_periods' WITH 'indexes' INTO A DICTIONARY (periodDict)
    periodDict = dict(zip(formatted_periods, idx_formatted_periods))
    
#     # CREATING A DICTIONARY FOR NEWLY ADDED TRANSACTION (including all relevant details)
#     txnDict = dict(date=dateEntry, debit=debit_entry_variable.get(),
#                    credit=credit_entry_variable.get(), period=periodEntry)
    
    # STORING THE DATAFRAME COLUMNS IN VARIABLES - FOR EASE
    txnDates = dfRow['DATE']
    txnDebits = dfRow['DEBIT']
    txnCredits = dfRow['CREDIT']
    
    # CONVERTS THE INPUTTED DATE INTO A 'datetime.date' TYPE
    # SO THAT IT CAN BE COMPARED AGAINST OTHER DATES
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
        
    # THIS STORES THE 'higher' FORMATTED PERIODS, (COMPARED TO PERIOD RELATING TO THE NEWLY ADDED TXN)
    # IT STORES THESE 'higher' PERIODS INTO A LIST CALLED 'firstPeriods'   
    for key, value in periodDict.items():
        if value > periodNo:
            firstPeriods.append(key)
        else:
            pass
   
    # ASSIGNS THE CURRENT PERIOD, AS A FILTER, TO THE CURRENT DATAFRAME
    for index, date in txnDates.items():
        if date == desiredDate:
            periodMask = dfRow['PERIOD'][index]
            print(dfRow['PERIOD'][index])
        else:
            pass      
        
    # TURNING DATAFRAME TO DICTIONARY, SO TXN VALUES CAN BE EDITED FROM RECORDS
    dataDict = dfRow.to_dict('dict')
    
    # UPDATES THE ADDED TRANSACTION FOR THE "DEBIT" & "CREDIT" COLUMNS
    # RECALL THAT 'txnDates' IS OF CLASS - class 'pandas.core.series.Series'>
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
            
        else:
            pass

    # TURNING THE DICTIONARY BACK INTO A DATAFRAME, AS NEW TXN VALUES NEED TO BE CEMENTED IN                               
    dfRow = dfRow.from_dict(dataDict)    
        
    # RESTATING THE DATAFRAME COLUMNS'S CONDITIONS - FOR THE NEWLY ADDED 'DEBIT' & 'CREDIT' ENTRIES                                 
    dfRow['DEBIT'] = dfRow['DEBIT'].round(decimals=2)
    dfRow['CREDIT'] = dfRow['CREDIT'].round(decimals=2)
    
    # (&) CREATING THE 'PERIOD' COLUMN, BY MAPPING THE RELEVANT 'PERIOD' FOR EACH DAY/DATE
    periods = []
    for row in dfRow['DATE']:
        for x in range(18):
            # IF THE 'row' (DATE) IS BETWEEN THE BOUNDS FOR THE 'FORMATTED PERIOD'
            # THEN INLCUDE THAT 'FORMATTED PERIOD' TO THE GIVEN DATES IN THE 'PERIOD COLUMN'                             
            if (row >= defined_periods[x][0]) & (row <= defined_periods[x][1]):
                periods.append(formatted_periods[x])
            else:
                pass
    dfRow['PERIOD'] = periods 
    
    # FILTERING THE DATAFRAME BASED ON THE 'PERIOD' OF THE INPUTTED DATE
    filterMask = (dfRow['PERIOD'] == periodMask)
    
    # APPLIES/PROCESSES THE FILTER OF THE PERIOD, TO THE DATAFRAME
    dfRow = dfRow[filterMask]     
    
    # ASSIGNING THE DATAFRAME 'BALANCE' ONCE ITS BEEN FILTERED FOR ITS PERIOD
    dfRow['BALANCE'] = (dfRow['DEBIT'].cumsum() +
                        dfRow['CREDIT'].cumsum()).round(decimals=2)
    
    # ASSIGNING THE DATAFRAME 'INTEREST' ONCE ITS BEEN FILTERED FOR ITS PERIOD
    dfRow['INTEREST'] = round(
        dfRow['BALANCE'] * dfRow['DAILY INTEREST'] * (1/100), 2)
       
    # STORING THE 'Total Interest' INTO A VARIABLE, OF THE GIVEN 'PERIOD'.
    interestSum2 = dfRow['INTEREST'].sum()
    
    # EXTRACTING THE CHANGE IN INTEREST ACCRUED, DUE TO THE NEW TXN ADDED 
    interestDifferential = interestSum2 - interestSum1
    interestDifferential = pd.to_numeric(interestDifferential, downcast='float')
    interestDifferential = interestDifferential.round(decimals=2)
    
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
    
    # ONLY INSERTS THE NEWLY UPDATED DATAFRAME VALUES INTO THE TKK.TREEVIEW WIDGET
    print("\n\n", "dfRow:__ ", "\n\n", dfRow)
    for index, row in dfRow.iterrows():
        tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT'], row['BALANCE'], row['INTEREST']])
        
    # AFTER THE ADDED TXN, INSERTING THE 'Total Interest' VALUE INTO THE BOTTOM OF THE TTK.TREEVIEW WIDGET TABLE.
    tv.insert('', 'end', values=["", "", "", "TOTAL INTEREST (AFTER TXN):", interestSum2])
    
    
    # BEFORE THE ADDED TXN, THIS INSERTS THE 'Total Interest' VALUE INTO THE TTK.TREEVIEW WIDGET
    tv.insert('', 'end', values=["", "", "",
                                 "TOTAL INTEREST (B4 TXN):", interestSum1])
    
    # INSERTS THE 'Change in Interest' VALUE INTO THE TTK.TREEVIEW WIDGET
    tv.insert('', 'end', values=["", "", "",
                                 "CHANGE IN INTEREST:", interestDifferential])
    
# ________________________________________________________________________________________________________________        

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
                  show="headings", height="38")

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
    tv.insert('', 'end', values=[row['DATE'], row['DEBIT'], row['CREDIT'], row['BALANCE'], row['INTEREST']])
    
# INSERTING THE 'Total Interest', INTO THE INITIAL DATAFRAME
tv.insert('', 'end', values=["", "", "", "TOTAL INTEREST:", interestSum]) 


# THE METHOD ON THE MAIN WINDOW WHICH WE EXECUTE WHEN WE WANT TO RUN OUR MAIN PROGRAM
# This method will loop forever, waiting for events from the user...
guiWindow.mainloop()
# ________________________________________________________________________________________________________________

