import os
import sqlite3

from xlsxwriter import Workbook
from Database import SetUpFile


def saveSnapshot():
    # take snapshot before importing files.
    conn = sqlite3.connect(SetUpFile.DBName)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_DB)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBArchiveName)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_Archive)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBLog)

    # Create a file object to store the snapshot
    snapshot_file = sqlite3.connect(SetUpFile.Snap_DBLog)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()


def convertToExcel(tableName, Database, RemoveFirstColumn=True):
    workbook = Workbook(SetUpFile.ExcelFileName)
    worksheet = workbook.add_worksheet()
    # Write column names to the worksheet
    col = __getColumnName(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    print(col)
    data = __getData(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    print(data)
    for col_num, column_name in enumerate(col):
        worksheet.write(0, col_num, column_name)

    for i, row in enumerate(data, 1):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
    workbook.close()
    os.system(SetUpFile.ExcelFileName)


def __getColumnName(tableName, Database, RemoveFirstColumn=True):
    # Open a connection to the database
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info('{0}')".format(tableName))
    columns = [column[1] for column in cursor.fetchall()]
    # remove first element
    if RemoveFirstColumn is True:
        columns.pop(0)
    conn.close()
    return columns


def __getData(tableName, Database, RemoveFirstColumn=True):
    # Open a connection to the database
    columns = __getColumnName(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute('SELECT {} FROM {}'.format(', '.join(columns), tableName))
    data = cursor.fetchall()
    conn.close()
    return data


def __ClearArchive():
    from Database import Archive
    UserArchive = Archive.UserArchive()
    InvestmentArchive = Archive.InvestmentArchive()
    UserArchive.dropTable()
    InvestmentArchive.dropTable()


def ClearTables():
    from Database import Log
    Log = Log.Log()
    Log.dropTable()
    __ClearArchive()


def previousStage(num=None):
    from Database import Log
    Log = Log.Log()
    if num is not None:
        for i in range(0, num):
            Log.previousStage()
    else:
        Log.previousStage()
