import os
import sqlite3

from xlsxwriter import Workbook

DBName = 'Database.db'

ExcelFileName = "Excel.xlsx"

DBArchiveName = 'DBSupportFiles/Archive.db'

DBLog = 'DBSupportFiles/Log.db'

Snap_DB = 'DBSnapshot/SnapDatabase.db'

Snap_Archive = 'DBSnapshot/SnapArchive.db'

Snap_DBLog = 'DBSnapshot/SnapDBLog.db'


def convertToExcel(tableName, Database):
    workbook = Workbook(ExcelFileName)
    worksheet = workbook.add_worksheet()
    # Write column names to the worksheet
    col = getColumnName(tableName, Database)
    print(col)
    data = getData(tableName, Database)
    print(data)
    for col_num, column_name in enumerate(col):
        worksheet.write(0, col_num, column_name)

    for i, row in enumerate(data, 1):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
    workbook.close()
    os.system(ExcelFileName)


def getColumnName(tableName, Database):
    # Open a connection to the database
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info('{0}')".format(tableName))
    columns = [column[1] for column in cursor.fetchall()]
    conn.close()
    return columns


def getData(tableName, Database):
    # Open a connection to the database
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {0}".format(tableName))
    data = cursor.fetchall()
    print(data)
    conn.close()
    return data
