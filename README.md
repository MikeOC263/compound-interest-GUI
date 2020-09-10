# compound-interest-GUI

## Purpose
This GUI relates to the compound interest that is accrued from a typical credit card.
The purpose of this program was to demonstrate to myself how different transactions would impact the _daily_ _balance_ and consequent _daily_ _interest_, which is calculated based on the _accounting_  _period_.


## GUI Functions
- _sheetPicker_, allows you to interchange which accounting period is shown in the GUI.

![001 sheetPicker](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/001%20sheetPicker.png)
![001 sheetPicker2](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/001%20sheetPicker2.jpg)


- _rowPicker_, allows you to include new transactions to the database.

![002 rowPicker](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/002%20rowPicker.png)


## Requirements
- This GUI extracts from a database which consists of a _.xlsx_ file, which should have it's _file_ _path_ & _file_ _name_ adjusted accordingly.

![003 Database File Path](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/003%20Database%20File%20Path.png)

- This file should have three columns labelled; _DATE_, _DEBIT_ & _CREDIT_ - in order to extract the data correctly.

![004 .xlsx Database](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/004%20.xlsx%20database.png)


## Assumptions
- This is based of an _annual_ _interest_ _rate_ of 21.87 %.

![005 Annual Interest](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/005%20Annual%20Interest%20.png)

- The _daily_ _balance_ and _daily_ _interest_ is calculated based on it's _accounting period_.

![006 Period Mask](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/006%20Period%20Mask.png)

- The _accounting_ _period_ within this program is based on the 8th - 7th of every month (unless those end dates fall on a weekend, rather than a weekday).

![007 Period Start Date](https://github.com/MikeOC263/compound-interest-GUI/blob/master/screenshots/007%20Period%20Start%20Date.png)





